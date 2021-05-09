pragma solidity >=0.4.21 <0.7.0;


contract Fundraiser{
    string public name;

    constructor(string memory _name) public {
        name = _name;
    }
    
}