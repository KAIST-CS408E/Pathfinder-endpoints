from chalicelib.helpers import credential
from aiohttp import BasicAuth

__NEO4J_CONFIG = {
    "host": "http://ec2-52-79-58-22.ap-northeast-2.compute.amazonaws.com",
    "port": "7474",
    "headers": {
        "Accept": "application/json",
        "charset": "UTF-8",
        "Content-Type": "application/json"
    },
    "username": credential.NEO4J_CREDENTIAL["username"],
    "password": credential.NEO4J_CREDENTIAL["password"]
}

NEO4J_URL = "%s:%s/%s/" % (__NEO4J_CONFIG["host"], __NEO4J_CONFIG["port"], "db/data/cypher")
NEO4J_HEADERS = __NEO4J_CONFIG["headers"]
NEO4J_AUTH = BasicAuth(__NEO4J_CONFIG["username"], __NEO4J_CONFIG["password"])
NEO4J_AUTH_T = (__NEO4J_CONFIG["username"], __NEO4J_CONFIG["password"])
