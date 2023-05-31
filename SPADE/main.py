from spade import agent

if __name__ == '__main__':
    agent = agent("your_jid@your_xmpp_server", "your_password")
    agent.start()
    agent.web.start(hostname="127.0.0.1", port="10000")

