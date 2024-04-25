import json
import asyncio
import time
from web3 import Web3
from web3 import HTTPProvider
from web3.contract.contract import Contract, ContractEvent
from redis import Redis
from rq import Queue
from rich.console import Console
from brodcast import startDepositBroadcast, startEmergencyWithdrawBroadcast, startWithdrawBroadcast
from datetime import timedelta

console = Console()

console.log("Connecting to Redis")
redis_connection = Redis(
    host="host.docker.internal"
)
console.log("Create new redis queue")
queue_connection = Queue(connection=redis_connection)

console.log("Reading staking artifacts")
contract_abi = []
contract_address = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"
with open("artifacts/staking.json") as File:
    artifact = json.loads(File.read())
    contract_abi = artifact['abi']

console.log("Connection to rpc provider")
provider = Web3(
    HTTPProvider("https://mainnet.infura.io/v3/c47fcf77394e40e78eac21970ed5feeb")
)

console.log("Connection to smart contract")
contract: Contract = provider.eth.contract(contract_address, abi=contract_abi)

async def getStakeDuration():
    stakeDuration = contract.functions.lockDuration().call()
    return stakeDuration


async def getStakeApy():
    stakeApy = contract.functions.apy().call()
    return stakeApy


async def getTotalStaked():
    totalStaked = contract.functions.totalStaked().call()
    return totalStaked


async def handle_deposit_event(event_filter, poll_interval: int):
    console.log("Handling deposit event")
    while True:
        for deposit in event_filter.get_new_entries():
            deposit_json = json.loads(provider.to_json(deposit))
            lockDuration = await getStakeDuration()
            stakeApy = await getStakeApy()
            totalStaked = await getTotalStaked()

            lockDuration = timedelta(seconds=float(lockDuration))
            console.print_json(provider.to_json(deposit))
            console.log("Start queue")
            queue_connection.enqueue(
                startDepositBroadcast,
                deposit_json['args']['amount'],
                lockDuration,
                stakeApy,
                totalStaked,
                deposit_json['transactionHash']
            )
            time.sleep(poll_interval / 1000)


async def handle_withdraw_event(event_filter, poll_interval: int, withdraw_type: str = "normal"):
    console.log(f"Handling {withdraw_type} withdraw event")
    while True:
        for withdraw in event_filter.get_new_entries():
            withdraw_json = json.loads(provider.to_json(withdraw))
            lockDuration = await getStakeDuration()
            stakeApy = await getStakeApy()
            totalStaked = await getTotalStaked()

            lockDuration = timedelta(seconds=float(lockDuration))
            if withdraw_type == "emergency":
                await startEmergencyWithdrawBroadcast(
                    withdraw['args']['amount'],
                    lockDuration,
                    stakeApy,
                    totalStaked,
                    withdraw_json['transactionHash']
                )
            else:
                await startWithdrawBroadcast(
                    withdraw['args']['amount'],
                    lockDuration,
                    stakeApy,
                    totalStaked,
                    withdraw_json['transactionHash']
                )


def main():
    console.log("Creating contract event")
    deposit_event_filter: ContractEvent = contract.events.Deposit.create_filter(
        fromBlock="latest")
    withdraw_event_filter: ContractEvent = contract.events.Withdraw.create_filter(
        fromBlock="latest")
    emergency_withdraw_event_filter: ContractEvent = contract.events.EmergencyWithdraw.create_filter(
        fromBlock="latest")

    console.log("Create asyncronous event loop")
    loop = asyncio.get_event_loop()
    try:
        console.log("Running function to handle deposit event")
        
        loop.run_until_complete(
            asyncio.gather(
                handle_deposit_event(deposit_event_filter, 200)
            )
        )
    finally:
        loop.close()


if __name__ == "__main__":
    main()
