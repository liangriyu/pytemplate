from flask import Blueprint

rpc_data = Blueprint('rpc_data', __name__)

from web_model import xxl_ctrl

