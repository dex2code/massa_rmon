app = {
   "cycle_duration_seconds": 15,
   "probes_per_cycle": 3,
}

telegram = {
   "nickname": "🤖 MASSA RM on {host_name} :",
   "message": "🏭 Node {node_name}: {node_status} \n\n {node_error}",
   "sending_delay_seconds": 2.1,
   "sending_timeout_seconds": 5,
}

nodes = {
   "LOCAL": "http://localhost:33035/api/v2",
   "REMOTE": "https://mainnet.massa.net/api/v2",
}

http = {
   "request_header": { 'content-type': 'application/json' },
   "request_payload": { 'id': 0, 'jsonrpc': '2.0', 'method': 'get_status', 'params': [] }
}

massa = {
   "find_key": "result"
}


if __name__ == "__main__":
   pass
