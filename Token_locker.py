metadata = Hash()
data = Hash(default_value=0)

@construct
def seed():
    metadata['operator'] = ctx.caller

@export
def change_metadata(key: str, new_value: str):
    assert ctx.caller == metadata['operator'], "only operator can set metadata"
    metadata[key] = new_value

@export
def new_locker(locker_id : str, contract: str, lock_until_year : int, lock_until_month : int, lock_until_day : int, ):

    assert bool(data[locker_id, 'locker_owner']) == False, "This match has already been created, please create one with a different name."
    assert lock_until_day != None, 'Must provide end day of lock!'
    assert lock_until_month != None, 'Must provide end month of lock!'
    assert lock_until_year != None, 'Must provide end year of lock!'
    assert datetime.datetime(year=lock_until_year, month=lock_until_month, day=lock_until_day) >= now, 'Lock end cannot be in the past!'

    data[locker_id, 'locker_owner'] = ctx.caller
    data[locker_id, 'contract'] = contract
    data[locker_id, 'staked_wallets'] = {}
    data[locker_id, 'total_locked'] = 0
    data[locker_id, 'end_date'] = datetime.datetime(year=lock_until_year, month=lock_until_month, day=lock_until_day, hour=0, minute=0, microsecond=0)

@export
def stake_token(locker_id: str, tokens_to_lock: float, contract: str):

    assert contract == data[locker_id, 'contract'], f"The contract does not match the token locker contract of {data[locker_id, 'contract']}."
    assert data[locker_id, 'end_date'] >= now, 'You can not stake in this locker since it has already ended.'

    staked_wallets = data[locker_id, 'staked_wallets']
    token = importlib.import_module(contract)
    token.transfer_from(amount=tokens_to_lock, to=ctx.this, main_account=ctx.caller)

    if ctx.caller not in staked_wallets:
        staked_wallets.update({ctx.caller: tokens_to_lock})
    else:
        staked_wallets[ctx.caller] += tokens_to_lock

    data[locker_id, 'staked_wallets'] = staked_wallets #adds the staker to the dict for calculating rewards for winners and losers
    data[locker_id, 'total_locked'] += tokens_to_lock #adds total CSTL to storage for calculating rewards

@export
def end_locker(locker_id: str):

    assert now >= data[locker_id, 'end_date'], f"This token locker has not ended yet. It will end on {data[locker_id, 'end_date']}."

    staked_wallets = data[locker_id, 'staked_wallets']
    token = importlib.import_module(contract)

    for key, value in dict(staked_wallets).items():
        token.transfer(amount=value, to=key)

    data[locker_id, 'locker_owner'] = None
    data[locker_id, 'contract'] = None
    data[locker_id, 'staked_wallets'] = {}
    data[locker_id, 'total_locked'] = 0
    data[locker_id, 'end_date'] = None

