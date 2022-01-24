@export
def stake_CSTL(match_id: str, IN_CSTL: int=0, AR_CSTL: int=0, HI_CSTL: int=0, CA_CSTL: int=0,  CP_CSTL: int=0):

#check to see if match is private. If public, don't check the list. If private, check to see if the player is on player list.
    if data[match_id, 'private'] == 1:
        playerlist = data[match_id, 'players']
        assert ctx.caller in playerlist, 'You are not on the list of players for this match. Contact the match creator if you wish to join.'

    staked_wallets = data[match_id, 'cstl_staked_wallets']
    cstl = importlib.import_module(cstl_contract.get())
    UNITS_PER_CSTL = metadata['UNITS_PER_CSTL']
    L_units = data[match_id, 'L_units']

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

    data[match_id, 'cstl_staked_wallets'] = staked_wallets #adds the staker to the dict for calculating rewards for winners and losers
    data[match_id, 'total_cstl'] += cstl_amount #adds total CSTL to storage for calculating rewards

#add input for contract name for the token to be locked

@export

def new_match(match_id : str, terrain: int, private : bool):


    assert bool(data[match_id, 'match_owner']) == False, "This match has already been created, please create one with a different name."

    data[match_id, 'match_owner'] = ctx.caller
    data[match_id, 'private'] = private
    data[match_id, 'players'] = [ctx.caller]
    data[match_id, 'terrain'] = terrain

    data[match_id, 'cstl_staked_wallets'] = {}
    data[match_id, 'fort_staked_wallets'] = {}

    data[match_id, 'L_units'] = {
        "IN": 0,
        "AR": 0,
        "HI": 0,
        "CA": 0,
        "CP": 0
    }

    data[match_id, 'D_units'] = {
        "GO": 0,
        "OA": 0,
        "OR": 0,
        "WO": 0,
        "TR": 0
    }

@export
def add_players(match_id : str, add1: str='', add2: str='', add3: str='', add4: str=''):

    assert data[match_id, 'match_owner'] == ctx.caller, 'You are not the match creator and cannot add players to this match.'
    assert data[match_id, 'private'] == True, 'This is a public game and individual players cannot be added.'

    addlist = [add1, add2, add3, add4]
    playerlist = data[match_id, 'players']

    for x in addlist:
        playerlist.append(x)

    data[match_id, 'players'] = playerlist

