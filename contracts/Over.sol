// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;
//pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Over is VRFConsumerBase, Ownable {
    AggregatorV3Interface internal ethUsdPriceFeed;
    uint256 public randomness;
    //address payable[] public players;
    //address[] public winners;
    bytes32 private keyhash;
    uint256 private fee;
    event RequestedRandomness(bytes32 requestId);

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        keyhash = _keyhash;
        fee = _fee;
    }

    function getUsdPrice() public view onlyOwner returns (uint256 price) {
        int256 answer;

        (, answer, , , ) = ethUsdPriceFeed.latestRoundData();

        return (uint256(answer));
    }

    function requestRandomness() public returns (bytes32 _random) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        emit RequestedRandomness(requestId);
        return _random;
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(_randomness > 0, "random-not-found");
        //uint256 indexOfWinner = _randomness % players.length;
        //recentWinner = players[indexOfWinner];
        //recentWinner.transfer(address(this).balance);
        // Reset
        //players = new address payable[](0);
        randomness = _randomness;
    }
}
