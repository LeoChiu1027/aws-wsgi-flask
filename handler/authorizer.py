import jwt

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 20

def handler(event, context):
    jwt_token = event.get('authorizationToken')
    print('event-----------')
    print(event)
    print('jwt_token-----------')
    print(jwt_token.split(' ')[1])

    if not jwt_token:
        print('no token------------')
        return {
            'message': 'token not found!'
        }, 401   

    try:
        payload = jwt.decode(jwt_token.split(' ')[1], JWT_SECRET,
                                algorithms=[JWT_ALGORITHM])
        print('payload--------------')
        print(payload)
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        print('decode error-----------------')
        return {'message': 'Token is invalid'}, 400

    if jwt_token:
        policy = generate_policy(
            payload['user_id'], 
            'Allow', 
            event['methodArn']
        )
        return policy
    else:
        print('deny---------------')
        policy = generate_policy(
            payload['user_id'],
            "Deny",
            event['methodArn']
        )
        return policy

def generate_policy(principal_id, effect, resource, scopes=None):
    policy = {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource
                }
            ]
        }
    }
    if scopes:
        policy['context'] = {'scopes': scopes}
    return policy