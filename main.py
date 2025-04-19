# !/usr/bin/env python
import logging
import multiprocessing
# import argparse
import dingtalk_stream
from app.api.dingtalk_client import DingTalkClient
import dingtalk_stream
from app.config.settings import settings
from app.utils.logger import setup_logger

def start_dingtalk_connection(logger):
    credential = dingtalk_stream.Credential(settings.CLIENT_ID, settings.CLIENT_SECRET)
    client = dingtalk_stream.DingTalkStreamClient(credential)
    client.register_callback_handler(dingtalk_stream.graph.GraphMessage.TOPIC, DingTalkClient(logger))
    client.start_forever()

def start_mcp_server(logger):
    """Start MCP server"""
    logger.info("Starting MCP server...")
    from app.core.mcp_server import mcp
    mcp.run(transport="stdio")

def main():
    logger = setup_logger(logging.INFO)
    """Start the MCP server in a separate process"""
    mcp_process = multiprocessing.Process(target=start_mcp_server)
    mcp_process.daemon = True
    mcp_process.start()
    """Start DingTalk connection"""
    start_dingtalk_connection(logger)

if __name__ == '__main__':
    main()
