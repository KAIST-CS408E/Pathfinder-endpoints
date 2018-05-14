from . import credential

NEO4J_CONFIG = {
    "host": "http://ec2-13-209-21-148.ap-northeast-2.compute.amazonaws.com",
    "port": "7474",
    "headers": {
        "Accept": "application/json",
        "charset": "UTF-8",
        "Content-Type": "application/json"
    },
    "username": credential.NEO4J_CREDENTIAL["username"],
    "password": credential.NEO4J_CREDENTIAL["password"]
}

REDIS_CONFIG = {
    "host": "http://ec2-13-209-21-148.ap-northeast-2.compute.amazonaws.com",
    "port": "6379",
    "username": credential.REDIS_CREDENTIAL["username"],
    "password": credential.REDIS_CREDENTIAL["password"]
}
