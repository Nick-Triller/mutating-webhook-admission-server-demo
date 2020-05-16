from flask import Flask, request, jsonify
import json
import base64

app = Flask(__name__)

injectContainerName = 'injected-sidecar'
# Prepare patch
containerManifestPatch = [{
    'op':    'add',
    'path':  '/spec/containers/-',
    'value': {
        'image': 'containous/whoami:v1.5.0',
        'imagePullPolicy': 'Always',
        'name': injectContainerName,
        'args': ['--port', '7777']
    }
}]
containerManifestPatchBytes = json.dumps(containerManifestPatch).encode()
containerManifestPatchSerialized = base64.b64encode(containerManifestPatchBytes).decode() 

@app.route('/', methods=['GET', 'POST'])
def mutate():
    if request.method == 'GET':
        return 'Hello, World!'  
    # Unmarshal
    admissionReview = request.get_json(force=True)

    # Allow request
    admissionReview['response'] = {
        'uid': admissionReview['request']['uid'],
        'allowed': True
    }
    # Don't mutate if the pod already has a container with the given name
    for container in admissionReview['request']['object']['spec']['containers']:
        if container['name'] == injectContainerName:
            return jsonify(admissionReview)
    # Add patch
    admissionReview['response']['patchType'] = 'JSONPatch'
    admissionReview['response']['patch'] = containerManifestPatchSerialized
    # Send response
    return jsonify(admissionReview)
