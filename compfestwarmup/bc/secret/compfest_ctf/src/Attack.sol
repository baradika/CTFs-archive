// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

interface ISecret {
    function guess(string calldata sentence, string calldata referrer) external payable;
    function ReferedBy() external pure returns (string memory);
}

contract Attack {
    ISecret public immutable challenge;
    
    constructor(address _challengeAddress) {
        challenge = ISecret(_challengeAddress);
    }
    
    function solve() external payable {
        string memory referrer = challenge.ReferedBy();
       	string memory sentence = "Can i join COMPFEST 17? Here is my secret number: 198514";
        challenge.guess{value: 0.5 ether}(sentence, referrer);
    }
}
