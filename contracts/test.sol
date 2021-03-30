pragma solidity >=0.4.0 <0.9.0;

contract Test{

    struct Reward {
        string name;
        string name2;
        uint val;
    }

    Reward[] public rewards;

    function addRewards(
        string memory _name, 
        string memory _name2,
        uint _val
    )
    public
    returns(uint)
    {
        rewards.push(
            Reward({
                name: _name,
                name2: _name2,
                val: _val
            })
        );
        uint newId = rewards.length;
        newId = newId + 1;
        return newId;
    }
}