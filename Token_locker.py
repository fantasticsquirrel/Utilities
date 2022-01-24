@export
def stake_CSTL(locker_id: str, IN_CSTL: int=0, AR_CSTL: int=0, HI_CSTL: int=0, CA_CSTL: int=0,  CP_CSTL: int=0):

#check to see if match is private. If public, don't check the list. If private, check to see if the player is on player list.
    if data[locker_id, 'private'] == 1:
        playerlist = data[locker_id, 'players']
        assert ctx.caller in playerlist, 'You are not on the list of players for this match. Contact the match creator if you wish to join.'

    staked_wallets = data[locker_id, 'staked_wallets']
    cstl = importlib.import_module(cstl_contract.get())
    UNITS_PER_CSTL = metadata['UNITS_PER_CSTL']
    L_units = data[locker_id, 'L_units']

    IN_amount = UNITS_PER_CSTL["IN"] * IN_CSTL
    AR_amount = UNITS_PER_CSTL["AR"] * AR_CSTL
    HI_amount = UNITS_PER_CSTL["HI"] * HI_CSTL
    CA_amount = UNITS_PER_CSTL["CA"] * CA_CSTL
    CP_amount = UNITS_PER_CSTL["CP"] * CP_CSTL

    cstl.transfer_from(amount=cstl_amount, to=ctx.this, main_account=ctx.caller)

    if ctx.caller not in staked_wallets:
        staked_wallets.update({ctx.caller: cstl_amount})
    else:
        staked_wallets[ctx.caller] += cstl_amount

    data[locker_id, 'staked_wallets'] = staked_wallets #adds the staker to the dict for calculating rewards for winners and losers
    data[locker_id, 'total_cstl'] += cstl_amount #adds total CSTL to storage for calculating rewards

#add input for contract name for the token to be locked

@export

def new_locker(locker_id : str, contract: str, lock_until_year :int, lock_until_month :int, lock_until_day :int, ):

    assert bool(data[locker_id, 'match_owner']) == False, "This match has already been created, please create one with a different name."

    data[locker_id, 'locker_owner'] = ctx.caller

    data[locker_id, 'staked_wallets'] = {}


@export
def add_players(locker_id : str, add1: str='', add2: str='', add3: str='', add4: str=''):

    assert data[locker_id, 'match_owner'] == ctx.caller, 'You are not the match creator and cannot add players to this match.'
    assert data[locker_id, 'private'] == True, 'This is a public game and individual players cannot be added.'

    addlist = [add1, add2, add3, add4]
    playerlist = data[locker_id, 'players']

    for x in addlist:
        playerlist.append(x)

    data[locker_id, 'players'] = playerlist

