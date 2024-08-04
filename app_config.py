app = {
   "cycle_duration_seconds": 15,
   "probes_per_cycle": 3,
}

telegram = {
   "nickname": "🤖 MASSA RM:",
   "message": "🏭 Node {node_name}: {node_status}",
   "sending_delay_seconds": 2.1,
   "sending_timeout_seconds": 5,
}

nodes = {
   "ZORG": "https://zorg.ek.pp.ru/massa"
}

http = {
   "request_header": { 'content-type': 'application/json' },
   "request_payload": { 'id': 0, 'jsonrpc': '2.0', 'method': 'get_status', 'params': [] }
}

massa = {
   "chain_id": 77658377
}


if __name__ == "__main__":
   pass
