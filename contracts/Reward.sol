pragma solidity >=0.4.0 <0.9.0;

import "./CrowdCoin.sol";
import "OpenZeppelin/openzeppelin-contracts@3.0.0/contracts/access/Ownable.sol";
// import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v3.4.0/contracts/access/Ownable.sol";

contract Reward is Ownable{
    using SafeMath for uint;
    using SafeMath for uint256;

    struct SurveyReward {
        address survey_owner;
        uint256 budget;
        uint256 target_number;
        uint top_perform_threshold;
        uint low_perform_threshold;
        uint256 max_reward;
    }

    CrowdCoin crowdcoin;
    address public contract_address;
    address public crowdcoin_address;
    uint256 public create_survey_cost;
    
    mapping(string => SurveyReward) public survey_rewards; //public survey key -> survey reward
    mapping(address => uint256) public dp_staking_rewards;
    address[] dp_stack;

    event Log_checksum(string survey_key, string space, string checksum);

    constructor () public Ownable(){
        // SAMPLE RECORD
        add_survey_reward(
            address(this),
            "PUBLIC_KEY",
            10000,
            1000,
            75,
            25
        );
        
        contract_address = address(this);
    }

    function set_coin(address _address) public onlyOwner{
        // SET COIN CONTRACT
        crowdcoin_address = _address;
        crowdcoin = CrowdCoin(crowdcoin_address);
        crowdcoin.set_reward_contract_address(contract_address);
        crowdcoin.init_mint();  //this contract account will have 10000000000 coins at the beginning
    }

    function get_max_reward(uint256 budget, uint256 target_number) public pure returns(uint256){
        return budget / target_number;
    }

    function add_survey_reward(
        // SET CONTRACT REWARD DETAILS WHEN SURVEY IS CREATED
        address _survey_owner,
        string memory survey_public_key,
        uint256 _budget,
        uint256 _target_number,
        uint _top_perform_threshold,
        uint _low_perform_threshold
        )public{
            uint256 _max_reward = get_max_reward(_budget, _target_number);
            // uint256 _min_reward_multiplier = get_min_reward(_top_perform_threshold, _budget);
            // uint256 _med_reward_multiplier = get_med_reward(_top_perform_threshold, _max_reward);

            survey_rewards[survey_public_key] = SurveyReward({
                survey_owner : _survey_owner,
                budget : _budget,
                target_number : _target_number,
                top_perform_threshold : _top_perform_threshold,
                low_perform_threshold : _low_perform_threshold,
                max_reward : _max_reward
                // min_reward_multiplier : _min_reward_multiplier,
                // med_reward_multiplier : _med_reward_multiplier
            });
        }

    function calculate_reward(address dp_address, string memory survey_key, uint256 performance)public onlyOwner{
        // CALCULATE REWARD OF DATA PROVIDERS BASED ON THEIR PERFORMANCE
        uint256 reward;
        SurveyReward memory survey = survey_rewards[survey_key];
        if (performance >= survey.top_perform_threshold){
            reward = survey.max_reward;
        }else if (performance <= survey.low_perform_threshold){
            reward = (performance * survey.budget) / (survey.target_number * 3 * survey.top_perform_threshold);
        }else{
            reward = (performance * survey.budget) / (survey.target_number * survey.top_perform_threshold);
        }
        dp_staking_rewards[dp_address] = dp_staking_rewards[dp_address] + reward;
        dp_stack.push(dp_address);
    }

    function get_dp_stacking(address dp_address) public view returns(uint256){
        return dp_staking_rewards[dp_address];
    }

    function distribute_all_rewards() public onlyOwner{
        //DISTRIBUTE ALL RECORDED REWARDS AT ONCE (not by survey, probably will call this function every 15 minutes and will transfer all rewards accumulated within the 15 mins)
        for(uint i=0; i<dp_stack.length; i++){
            address dp = dp_stack[i];
            uint256 received_rewards = dp_staking_rewards[dp] * (1 ether); // if not ganache
            // uint256 received_rewards = dp_staking_rewards[dp]; // if ganache
            if (received_rewards > 0){
                crowdcoin.transferFrom(contract_address, dp, received_rewards);
            }
            dp_staking_rewards[dp] = 0; //reset dp_staking_rewards balance
        }
        delete dp_stack; //reset dp_stack records
    }

    function create_survey(
        address survey_owner_address,
        string memory survey_public_key,
        uint256 _budget,
        uint256 _target_number,
        uint _top_perform_threshold,
        uint _low_perform_threshold) public {
            // uint256 sum;
            // sum = create_survey_cost + _budget;
            // // DEDUCT CREATE SURVEY COST + BUDGET FOT THE SURVEY
            // crowdcoin.transferFrom(survey_owner_address, contract_address, sum);
            add_survey_reward(survey_owner_address, survey_public_key, _budget, _target_number, _top_perform_threshold, _low_perform_threshold);
    }

    function purchase_coin(address purchase, uint256 amount) public onlyOwner{
        // ADDRESS THAT PURCHASED THE REWARD POINTS
        crowdcoin.transferFrom(contract_address, purchase, amount);
    }

    function get_survey_reward_by_key(
        // SET CONTRACT REWARD DETAILS WHEN SURVEY IS CREATED
        string memory survey_public_key
        )public view returns(
            address,
            uint256,
            uint256,
            uint,
            uint,
            uint256
            // uint256,
            // uint256
        ){
            SurveyReward memory s = survey_rewards[survey_public_key];
            return(
                s.survey_owner,
                s.budget,
                s.target_number,
                s.top_perform_threshold,
                s.low_perform_threshold,
                s.max_reward
                // s.min_reward_multiplier,
                // s.med_reward_multiplier
            );
        }
    
    function log_checksum(string memory survey_key, string memory space, string memory checksum) public{
        emit Log_checksum(survey_key, space, checksum);
    }

}