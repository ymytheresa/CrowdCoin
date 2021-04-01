// SPDX-License-Identifier: MIT

// import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v3.4.0/contracts/access/Ownable.sol";
// import "OpenZeppelin/openzeppelin-contracts@3.0.0/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@3.0.0/contracts/math/SafeMath.sol";
import "./ERC20.sol";


pragma solidity >=0.4.0 <0.9.0;

contract CrowdCoin is ERC20{
    address reward_contract_address;

    constructor () public ERC20("CrowdCoin", "CWC"){
        _mint(msg.sender, 100000 * (10 ** uint256(decimals())));
        // owner = msg.sender;
    }

    function set_reward_contract_address(address add)public{
        reward_contract_address = add;
    }

    function init_mint() public{
        _mint(reward_contract_address, 100000 * (10 ** uint256(decimals())));
    }

    function getBal(address bal) public view returns(uint256){
        return balanceOf(bal);
    }
}