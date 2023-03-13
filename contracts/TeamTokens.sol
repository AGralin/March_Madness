// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts@4.8.2/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts@4.8.2/security/Pausable.sol";
import "@openzeppelin/contracts@4.8.2/access/Ownable.sol";
import "@openzeppelin/contracts@4.8.2/token/ERC1155/extensions/ERC1155Burnable.sol";
import "@openzeppelin/contracts@4.8.2/token/ERC1155/extensions/ERC1155Supply.sol";

contract TeamTokens is ERC1155, Pausable,Ownable, ERC1155Burnable, ERC1155Supply {

    uint256 public constant TOKEN_PRICE = .005 ether; 
    uint256 public constant TRANSACTION_FEE = .001 ether;


    constructor() ERC1155("") {}


    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }
    // Mint th tokens and charge the ether
    function mint(address to, uint256 id, uint256 amount)
        payable
        public
    {   require(msg.value == amount * TOKEN_PRICE + TRANSACTION_FEE, "Incorrect Ether amount");
        require(id < 64, "Sorry that id does not exist, choose a number between 0 and 63");
        //mint the token
        _mint(to, id, amount, "");

        uint256 totalAmount = msg.value - TRANSACTION_FEE;
        //sent the ether to contract
        payable(address(this)).transfer(totalAmount);

        //pay the owner the transaction fee
        payable(owner()).transfer(TRANSACTION_FEE);
    }
    
    // receive the ether for the contract
    receive () external payable {

    }

    // Get the contract balance (pool)
    function getContractBalance() external view returns (uint256) {
        // Get the balance of the contract's address
        return address(this).balance;
    }

    function mintBatch(address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data)
        public
        onlyOwner
    {
        _mintBatch(to, ids, amounts, data);
    }

    function _beforeTokenTransfer(address operator, address from, address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data)
        internal
        whenNotPaused
        override(ERC1155, ERC1155Supply)
    {
        super._beforeTokenTransfer(operator, from, to, ids, amounts, data);
    }
}