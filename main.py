from bayesianAgent import BayesianAgent

def main():

    agent = BayesianAgent()

    msg = "Please forward us the following information of your credit card. Click this link"

    print(msg)

    agent.predict(msg)


if __name__ == "__main__":
    main()