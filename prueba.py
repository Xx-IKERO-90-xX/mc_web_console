from mcrcon import MCRcon

def test_connection(ip, port, passwd):
    try:
        with MCRcon(ip, passwd, port=port) as mcr:
            response = mcr.command("list")
            print(response)
    except Exception as e:
        print("connection failed:", e)

test_connection("protea.seedloaf.com", 49308, "f738684afcf4fd4dc49682e9")