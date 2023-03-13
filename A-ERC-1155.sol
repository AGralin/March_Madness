// SPDX-License-Identifier: MIT
/**
 __       __                                __                                 
|  \     /  \                              |  \                                
| $$\   /  $$  ______    ______    _______ | $$____                            
| $$$\ /  $$$ |      \  /      \  /       \| $$    \                           
| $$$$\  $$$$  \$$$$$$\|  $$$$$$\|  $$$$$$$| $$$$$$$\                          
| $$\$$ $$ $$ /      $$| $$   \$$| $$      | $$  | $$                          
| $$ \$$$| $$|  $$$$$$$| $$      | $$_____ | $$  | $$                          
| $$  \$ | $$ \$$    $$| $$       \$$     \| $$  | $$                          
 \$$      \$$  \$$$$$$$ \$$        \$$$$$$$ \$$   \$$                                                                             
 __       __                  __                                               
|  \     /  \                |  \                                              
| $$\   /  $$  ______    ____| $$ _______    ______    _______   _______       
| $$$\ /  $$$ |      \  /      $$|       \  /      \  /       \ /       \      
| $$$$\  $$$$  \$$$$$$\|  $$$$$$$| $$$$$$$\|  $$$$$$\|  $$$$$$$|  $$$$$$$      
| $$\$$ $$ $$ /      $$| $$  | $$| $$  | $$| $$    $$ \$$    \  \$$    \       
| $$ \$$$| $$|  $$$$$$$| $$__| $$| $$  | $$| $$$$$$$$ _\$$$$$$\ _\$$$$$$\      
| $$  \$ | $$ \$$    $$ \$$    $$| $$  | $$ \$$     \|       $$|       $$      
 \$$      \$$  \$$$$$$$  \$$$$$$$ \$$   \$$  \$$$$$$$ \$$$$$$$  \$$$$$$$
 */

pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Burnable.sol";
import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Supply.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract MarchMadness is ERC1155, Ownable, Pausable, ERC1155Burnable, ERC1155Supply {
    uint256 public publicPrice = 0.001 ether;
    bool public publicMintOpen = true;
    mapping(uint => string) public tokenURI;
    constructor() ERC1155("") {}

    // edit function to open/close public mint
    function editMintWindows(
        bool _publicMintOpen
    ) external onlyOwner {
        publicMintOpen = _publicMintOpen;
    }
    // pause function
    function pause() public onlyOwner {
        _pause();
    }
    // unpause function
    function unpause() public onlyOwner {
        _unpause();
    }
    // public mint function
    function mint(uint256 id, uint256 amount)
        public
        payable
    {
        require(publicMintOpen, "Public mint is closed");
        require(id < 64, "Sorry that id does not exist, choose a number between 0 and 63");
        require(msg.value == publicPrice * amount, "Not enough ETH");
        _mint(msg.sender, id, amount, "");
    }

    // withdraw function
    function withdraw(address _addr) external onlyOwner {
        uint256 balance = address(this).balance;
        payable(_addr).transfer(balance);
    }
    // set URI
    function setURI(uint _id, string memory _uri) external onlyOwner {
    tokenURI[_id] = _uri;
    emit URI(_uri, _id);
    }
    // call URI
    function uri(uint _id) public override view returns (string memory) {
    return tokenURI[_id];
    }

    /*
    // URI
    function uri(uint256 _id) public view virtual override returns (string memory) {
        require(exists(_id), "URI: nonexistent token");

        return string(abi.encodePacked(super.uri(_id), Strings.toString(_id), ".json"));
    }
    */

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