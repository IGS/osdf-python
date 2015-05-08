# osdf-python

    import pprint
    from osdf import OSDF

    server = "server.ip.dns.address"
    username = "user"
    password = "password"
    port = 8123

    osdf = OSDF(server, username, password, port)

    info = osdf.get_info()

    pprint.pprint(info)
