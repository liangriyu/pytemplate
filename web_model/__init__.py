from flask import Blueprint

rpc_api = Blueprint('rpc_api', __name__)

from web_model import xxl_ctrl

