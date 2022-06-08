//SPDX-License-Identifier:MIT
pragma solidity ^0.8.0;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import '@chainlink/contracts/src/v0.8/VRFConsumerBase.sol';

contract Lottery is VRFConsumerBase{

    address payable[] public players;
    uint256 public usdEntryFee;
    uint256 public randomness;
    uint256 public indexOfWinner;
    address payable public recentWinner;
    address public owner;
    AggregatorV3Interface internal ethUsdPriceFeed;

    enum LotteryState {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
	uint256 public fee;
    LotteryState public lotteryState;
    bytes32 public keyHash;
    event RequestedRandomness(bytes32 requestId);

    constructor(address _priceFeedAddress,
	address _vrfCoordinator,
	address _link,
	uint256 _fee,
    bytes32 _keyHash

	) public VRFConsumerBase(_vrfCoordinator, _link){
        usdEntryFee =50 *(10 **18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        owner = msg.sender;
        lotteryState = LotteryState.CLOSED;
        fee = _fee;
        keyHash = _keyHash;
    }


    modifier onlyOwner{
        require(msg.sender == owner);
        _;
    }

    function enter() public payable {
        require(lotteryState == LotteryState.OPEN);
        require(msg.value >= getEntranceFee(), "You need a minimum of 50 USD to enter lottery");
        players.push(payable(msg.sender));
    }


    function getEntranceFee()public view returns(uint256){
        //geting price date from chainlink
        (,int price,,,) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * (10 ** 10);

        uint costToEnter = (usdEntryFee * 10 ** 18) / adjustedPrice;
        return costToEnter;
    }

    function begin()public onlyOwner{
        require(
            lotteryState == LotteryState.CLOSED,
            "can't start lottery yet!"

        );
        lotteryState = LotteryState.OPEN;
    }

    function end() public onlyOwner{
        //require(lotteryState == LotteryState.CALCULATING_WINNER)
        require(LINK.balanceOf(address(this)) >= fee, "Not enough LINK - fill contract with faucet");
        bytes32 requestId = requestRandomness(keyHash, fee);

        

        //uint256()
           



        lotteryState = LotteryState.CALCULATING_WINNER;
        emit RequestedRandomness(requestId);
    }
    function fulfillRandomness(bytes32 _requestId, uint _randomness) internal override{
        require(lotteryState == LotteryState.CALCULATING_WINNER);
        require(_randomness > 0, "random-Value-not-found");

        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);
        players = new address payable[](0);
        lotteryState = LotteryState.CLOSED;
        randomness = _randomness;
    }
}
