%lang starknet
%builtins pedersen range_check ecdsa

from starkware.cairo.common.cairo_builtins import HashBuiltin, SignatureBuiltin
from starkware.starknet.common.syscalls import get_caller_address
from starkware.starknet.common.storage import Storage
from starkware.cairo.common.math import assert_nn_le, assert_lt, assert_not_zero

@storage_var
func owner(token_id: felt) -> (res: felt):
end

@storage_var
func balances(owner: felt) -> (nb: felt):
end

@storage_var
func balance_details(owner: felt, index: felt) -> (res: felt):
end

@storage_var
func initialized() -> (res: felt):
end

#### Specific bit

# Material encodes the rarity. Values range 1-16
@storage_var
func material(token_id: felt) -> (res: felt):
end

# Says if a brick is part of set
@storage_var
func part_of_set(token_id: felt) -> (res: felt):
end


@external
func initialize{
        storage_ptr: Storage*,
        pedersen_ptr: HashBuiltin*,
        syscall_ptr: felt*,
        range_check_ptr
    } ():
    let (_initialized) = initialized.read()
    assert _initialized = 0
    initialized.write(1)
    return ()
end

@view
func balance_of{
        storage_ptr: Storage*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    } (owner: felt) -> (res: felt):
    let (res) = balances.read(owner=owner)
    return (res)
end

@view
func owner_of{
        storage_ptr: Storage*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    } (token_id: felt) -> (res: felt):
    let (res) = owner.read(token_id=token_id)
    return (res)
end

@view
func token_data{
        storage_ptr: Storage*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    } (token_id: felt) -> (res: (felt, felt)):
    let (res) = owner.read(token_id=token_id)
    let (res2) = material.read(token_id=token_id)
    let tp = (res, res2)
    return (tp)
end

@view
func token_at_index{
        storage_ptr: Storage*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    } (owner: felt, index: felt) -> (res: felt):
    let (res) = balances.read(owner=owner)
    assert_lt(index, res)
    let (retval) = balance_details.read(owner=owner, index=index)
    return (retval)
end

func _mint{
        storage_ptr: Storage*,
        pedersen_ptr: HashBuiltin*,
        syscall_ptr: felt*,
        range_check_ptr
    } (recipient: felt, token_id: felt, mat: felt):
    let (curr_owner) = owner.read(token_id)
    assert curr_owner = 0
    let (res) = balances.read(owner=recipient)
    balances.write(recipient, res + 1)
    balance_details.write(recipient, res, token_id)
    owner.write(token_id, recipient)
    part_of_set.write(token_id, 0)
    material.write(token_id, mat)
    return ()
end

@external
func mint{
        storage_ptr: Storage*,
        pedersen_ptr: HashBuiltin*,
        syscall_ptr: felt*,
        range_check_ptr
    } (owner: felt, token_id: felt, material: felt):
    assert_not_zero(material)
    _mint(owner, token_id, material)
    return ()
end

@external
func set_part_of_set{
        storage_ptr: Storage*,
        pedersen_ptr: HashBuiltin*,
        syscall_ptr: felt*,
        range_check_ptr
    } (token_id: felt, set: felt):
    let (curr_set) = part_of_set.read(token_id)
    assert curr_set = 0
    let (caller) = get_caller_address()
    return ()
end

func find_item_index{
        storage_ptr: Storage*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    } (owner: felt, token_id: felt, cur_idx: felt, max: felt) -> (res: felt):
    alloc_locals
    local storage: Storage* = storage_ptr
    local pedersen: HashBuiltin* = pedersen_ptr
    local range_check = range_check_ptr
    let (ct) = balance_details.read(owner, cur_idx)
    if ct == token_id:
        return (cur_idx)
    end
    if cur_idx == max:
        return (0)
    end
    return find_item_index{storage_ptr=storage, pedersen_ptr=pedersen, range_check_ptr=range_check}(owner, token_id, cur_idx + 1, max)
end

func _transfer{
        storage_ptr: Storage*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    } (sender: felt, recipient: felt, token_id: felt):
    alloc_locals
    let (local curr_owner) = owner.read(token_id=token_id)
    assert curr_owner = sender
    # Cannot transfer a brick that's part of a set.
    let (curr_set) = part_of_set.read(token_id=token_id)
    assert curr_set = 0
    owner.write(token_id, recipient)

    # updating balances is annoying
    let (local cur) = balances.read(curr_owner)
    balances.write(curr_owner, cur - 1)

    #let (it) = find_item_index(curr_owner, token_id, 0, cur)
    #let (tok) = balance_details.read(curr_owner, cur - 1)
    #balance_details.write(curr_owner, it, tok)

    #let (rcur) = balances.read(recipient)
    #balances.write(recipient, rcur + 1)
    #balance_details.write(recipient, rcur, tok)

    return ()
end

@external
func transfer_from{
        storage_ptr: Storage*,
        pedersen_ptr: HashBuiltin*,
        syscall_ptr: felt*,
        range_check_ptr
    } (sender: felt, recipient: felt, token_id: felt):
    _transfer(sender, recipient, token_id)
    return ()
end


@view
func tokens_at_index{
        storage_ptr: Storage*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    } (owner: felt, index: felt) -> (
        ret0: felt,  rMat0: felt, rSet0: felt,
        ret1: felt,  rMat1: felt, rSet1: felt,
        ret2: felt,  rMat2: felt, rSet2: felt,
        ret3: felt,  rMat3: felt, rSet3: felt,
        ret4: felt,  rMat4: felt, rSet4: felt,
        ret5: felt,  rMat5: felt, rSet5: felt,
        ret6: felt,  rMat6: felt, rSet6: felt,
        ret7: felt,  rMat7: felt, rSet7: felt,
        ret8: felt,  rMat8: felt, rSet8: felt,
        ret9: felt,  rMat9: felt, rSet9: felt,
        ret10: felt, rMat10: felt, rSet10: felt,
        ret11: felt, rMat11: felt, rSet11: felt,
        ret12: felt, rMat12: felt, rSet12: felt,
        ret13: felt, rMat13: felt, rSet13: felt,
        ret14: felt, rMat14: felt, rSet14: felt,
        ret15: felt, rMat15: felt, rSet15: felt,
        ret16: felt, rMat16: felt, rSet16: felt,
        ret17: felt, rMat17: felt, rSet17: felt,
        ret18: felt, rMat18: felt, rSet18: felt,
        ret19: felt, rMat19: felt, rSet19: felt,
    ):
    alloc_locals
    let (res) = balances.read(owner=owner)
    assert_lt(index, res)
    let(local retval0: felt) = balance_details.read(owner=owner, index=index+0)
    let(local retval1: felt) = balance_details.read(owner=owner, index=index+1)
    let(local retval2: felt) = balance_details.read(owner=owner, index=index+2)
    let(local retval3: felt) = balance_details.read(owner=owner, index=index+3)
    let(local retval4: felt) = balance_details.read(owner=owner, index=index+4)
    let(local retval5: felt) = balance_details.read(owner=owner, index=index+5)
    let(local retval6: felt) = balance_details.read(owner=owner, index=index+6)
    let(local retval7: felt) = balance_details.read(owner=owner, index=index+7)
    let(local retval8: felt) = balance_details.read(owner=owner, index=index+8)
    let(local retval9: felt) = balance_details.read(owner=owner, index=index+9)
    let(local retval10: felt) = balance_details.read(owner=owner, index=index+10)
    let(local retval11: felt) = balance_details.read(owner=owner, index=index+11)
    let(local retval12: felt) = balance_details.read(owner=owner, index=index+12)
    let(local retval13: felt) = balance_details.read(owner=owner, index=index+13)
    let(local retval14: felt) = balance_details.read(owner=owner, index=index+14)
    let(local retval15: felt) = balance_details.read(owner=owner, index=index+15)
    let(local retval16: felt) = balance_details.read(owner=owner, index=index+16)
    let(local retval17: felt) = balance_details.read(owner=owner, index=index+17)
    let(local retval18: felt) = balance_details.read(owner=owner, index=index+18)
    let(local retval19: felt) = balance_details.read(owner=owner, index=index+19)

    let(local retMat0: felt) = material.read(token_id=retval0)
    let(local retMat1: felt) = material.read(token_id=retval1)
    let(local retMat2: felt) = material.read(token_id=retval2)
    let(local retMat3: felt) = material.read(token_id=retval3)
    let(local retMat4: felt) = material.read(token_id=retval4)
    let(local retMat5: felt) = material.read(token_id=retval5)
    let(local retMat6: felt) = material.read(token_id=retval6)
    let(local retMat7: felt) = material.read(token_id=retval7)
    let(local retMat8: felt) = material.read(token_id=retval8)
    let(local retMat9: felt) = material.read(token_id=retval9)
    let(local retMat10: felt) = material.read(token_id=retval10)
    let(local retMat11: felt) = material.read(token_id=retval11)
    let(local retMat12: felt) = material.read(token_id=retval12)
    let(local retMat13: felt) = material.read(token_id=retval13)
    let(local retMat14: felt) = material.read(token_id=retval14)
    let(local retMat15: felt) = material.read(token_id=retval15)
    let(local retMat16: felt) = material.read(token_id=retval16)
    let(local retMat17: felt) = material.read(token_id=retval17)
    let(local retMat18: felt) = material.read(token_id=retval18)
    let(local retMat19: felt) = material.read(token_id=retval19)
    
    let(local retSet0: felt) = part_of_set.read(token_id=retval0)
    let(local retSet1: felt) = part_of_set.read(token_id=retval1)
    let(local retSet2: felt) = part_of_set.read(token_id=retval2)
    let(local retSet3: felt) = part_of_set.read(token_id=retval3)
    let(local retSet4: felt) = part_of_set.read(token_id=retval4)
    let(local retSet5: felt) = part_of_set.read(token_id=retval5)
    let(local retSet6: felt) = part_of_set.read(token_id=retval6)
    let(local retSet7: felt) = part_of_set.read(token_id=retval7)
    let(local retSet8: felt) = part_of_set.read(token_id=retval8)
    let(local retSet9: felt) = part_of_set.read(token_id=retval9)
    let(local retSet10: felt) = part_of_set.read(token_id=retval10)
    let(local retSet11: felt) = part_of_set.read(token_id=retval11)
    let(local retSet12: felt) = part_of_set.read(token_id=retval12)
    let(local retSet13: felt) = part_of_set.read(token_id=retval13)
    let(local retSet14: felt) = part_of_set.read(token_id=retval14)
    let(local retSet15: felt) = part_of_set.read(token_id=retval15)
    let(local retSet16: felt) = part_of_set.read(token_id=retval16)
    let(local retSet17: felt) = part_of_set.read(token_id=retval17)
    let(local retSet18: felt) = part_of_set.read(token_id=retval18)
    let(local retSet19: felt) = part_of_set.read(token_id=retval19)
    return (
        ret0=retval0,   rMat0=retMat0,    rSet0=retSet0,
        ret1=retval1,   rMat1=retMat1,    rSet1=retSet1,
        ret2=retval2,   rMat2=retMat2,    rSet2=retSet2,
        ret3=retval3,   rMat3=retMat3,    rSet3=retSet3,
        ret4=retval4,   rMat4=retMat4,    rSet4=retSet4,
        ret5=retval5,   rMat5=retMat5,    rSet5=retSet5,
        ret6=retval6,   rMat6=retMat6,    rSet6=retSet6,
        ret7=retval7,   rMat7=retMat7,    rSet7=retSet7,
        ret8=retval8,   rMat8=retMat8,    rSet8=retSet8,
        ret9=retval9,   rMat9=retMat9,    rSet9=retSet9,
        ret10=retval10, rMat10=retMat10,  rSet10=retSet10,
        ret11=retval11, rMat11=retMat11,  rSet11=retSet11,
        ret12=retval12, rMat12=retMat12,  rSet12=retSet12,
        ret13=retval13, rMat13=retMat13,  rSet13=retSet13,
        ret14=retval14, rMat14=retMat14,  rSet14=retSet14,
        ret15=retval15, rMat15=retMat15,  rSet15=retSet15,
        ret16=retval16, rMat16=retMat16,  rSet16=retSet16,
        ret17=retval17, rMat17=retMat17,  rSet17=retSet17,
        ret18=retval18, rMat18=retMat18,  rSet18=retSet18,
        ret19=retval19, rMat19=retMat19,  rSet19=retSet19
    )
end

