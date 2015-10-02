import os
import hashlib
import random
import config

from flask import Flask, Response, jsonify, abort, make_response, request

from database import session
from models import Mp4Info, User

from hachoir_core.cmd_line import unicodeFilename
from hachoir_parser import createParser
from hachoir_metadata import extractMetadata

app = Flask(__name__)

### Adding test data into the database
test1 = Mp4Info(name='someMp4.mp4',
                width=380,
                height=480,
                mime_type='mp4',
                duration=70,
                owner='Client X',
                location='/clientX/'
                )

#session.add(test1)
#session.commit()

user1 = User(username='youngrya',
             password='ThisIsntSecure',
             email='ryoung@spiderhop.net',
             api_key=hashlib.sha224(str(random.getrandbits(256))).hexdigest())

#session.add(user1)
#session.commit()


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.close()


## Return a 404 when the client doesn't send request as json
@app.errorhandler(404)
def not_found(error):
    """
    Default 404 for non-json requests
    """

    return make_response(jsonify({'Error': 'Not Found'}), 404)


## Return a 405 for unauthorized when client doesn't provide valid API token
@app.errorhandler(405)
def not_authorized(error):
    """
    Default 405 for invalid Auth Token
    """

    return make_response(jsonify({'Error': 'Not Authorized'}), 405)


## TODO: Treat config in more flask / pythonic way
## TODO: Add sanity Checks - maybe even a fully fledged test suite...
## TODO: A safe upload file handler
## TODO: File Structure - probably don't want to store these in DocRoot
@app.route('/api/v1.0/mp4/upload', methods=['POST'])
def upload_mp4():
    if request.headers['Content-Type'].split(';')[0] != u'multipart/form-data':
        abort(404)

    user = session.query(User).filter_by(
        api_key=request.headers['X-Auth-Token']).first()

    if user is not None:
        f = request.files['files']
        f.save(os.path.join(config._upload_directory, f.filename))

        filename = os.path.join(config._upload_directory, f.filename)
        filename, realname = unicodeFilename(str(filename)), str(filename)
        parser = createParser(filename, realname)

        metadata = extractMetadata(parser)
        text = metadata.exportPlaintext()

        _file_data = {}

        for item in text[1:]:
            _file_data[item.split(':')[0].strip(' -')] = item.split(':')[1]

        _file_data['name'] = f.filename

        db_entry = Mp4Info(name=f.filename,
                           width=_file_data['Image width'],
                           height=_file_data['Image height'],
                           mime_type=_file_data['MIME type'],
                           duration=_file_data['Duration'],
                           owner=user.username,
                           location=os.path.join(config._upload_directory,
                                                 f.filename)
                           )

        session.add(db_entry)
        session.commit()

        return make_response(jsonify({'entry_id': db_entry.id,
                                      'name': db_entry.name,
                                      'width': db_entry.width,
                                      'height': db_entry.height,
                                      'mime_type': db_entry.mime_type,
                                      'duration': db_entry.duration,
                                      'owner': db_entry.owner,
                                      'upload_date': db_entry.upload_date}),
                             201)
    abort(405)


@app.route('/api/v1.0/mp4/download/<int:media_id>', methods=['GET'])
def get_media(media_id):
    user = session.query(User).filter_by(api_key=request.headers['X-Auth-Token']).first()
    media_file = session.query(Mp4Info).filter_by(id=media_id).first()

    if user:
        response = make_response(media_file.location)
        response.headers["Content-Disposition"] = "attachment; " + media_file.location
        #return make_response(jsonify({'username': user.username,
        #                              'media_id': media_id,
        #                              'file_location': media_file.location}))
        print response
        return Response(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

