//SPDX-License-Identifier:MIT
pragma solidity ^0.8.0;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import '@chainlink/contracts/src/v0.8/VRFConsumerBase.sol';

contract Lottery is VRFConsumerBase{

    address payable [] public players;
    uint256 usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    address owner;
    enum LotteryState {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LotteryState public lotteryState;

    constructor(address _priceFeedAddress, address _vrfCoordinator, address _link )
        public  VRFConsumerBase(_vrfCoordinator)
    {
         usdEntryFee =50 *(10 **18);
         ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
         owner = msg.sender;

    }


    modifier onlyOwner{
        require(msg.sender == owner);
        _;
    }

    function enter() public payable {
        require(lotteryState = LotteryState.OPEN);
        require(msg.value >= getEntranceFee(), "You need a minimum of 50 USD to enter lottery");
        players.push(msg.sender);
    }


    function getEntranceFee()public view returns(uint256){
        //geting price date from chainlink
        (,int price,,,) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * (10 ** 10);

        uint costToEnter = (usdEntryFee * 10 ** 18) / adjustedPrice;
        return costToEnter;
    }

    function begin()public onlyOwner{
        require(lotteryState == LotteryState.CLOSED);
    



        lotteryState = LotteryState.OPEN;
    }

    function end() public onlyOwner{
        require(lotteryState == LotteryState.OPEN);
        

        //uint256()
           



        lotteryState = LotteryState.CALCULATING_WINNER;
    }
    function fufillRandomness(bytes32 _requestId, uint _randomness) internal override{
        require(lotteryState == LotteryState.CALCULATING_WINNER);
        require(_randomness > 0, "random-Value-not-found");
    }

}
