// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract Me_Financio {
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public direccionesQueDepositan;
    address public duenoDelContrato;
    address[] public financiadores;
    AggregatorV3Interface public alimentadorDePrecio;

    constructor(address _alimentadorDePrecio) public {
        alimentadorDePrecio = AggregatorV3Interface(_alimentadorDePrecio);
        duenoDelContrato = msg.sender;
    }

    function fund() public payable {
        uint256 minimoUsd = 50 * 10**18;
        // 1GWEI < 50usd
        require(
            ObtenerRatioDeConversion(msg.value) >= minimoUsd,
            "El minimo a financiar son 50usd!"
        );
        direccionesQueDepositan[msg.sender] += msg.value;
        financiadores.push(msg.sender);
    }

    function obtenerDecimales() public view returns (uint256) {
        //AggregatorV3Interface alimentadorDePrecio = AggregatorV3Interface(
        //    0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e
        //);
        return alimentadorDePrecio.decimals();
    }

    function obtenerVersion() public view returns (uint256) {
        //AggregatorV3Interface alimentadorDePrecio = AggregatorV3Interface(
        //    0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e
        //);
        return alimentadorDePrecio.version();
    }

    function obtenerPrecio() public view returns (uint256) {
        //AggregatorV3Interface alimentadorDePrecio = AggregatorV3Interface(
        //    0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e
        //);
        (, int256 answer, , , ) = alimentadorDePrecio.latestRoundData();
        return uint256(answer * 1);
        //return uint256(answer);
    }

    // 100000000
    function ObtenerRatioDeConversion(uint256 cantidadEth)
        public
        view
        returns (uint256)
    {
        uint256 precioEth = obtenerPrecio();
        uint256 cantidadEthEnUsd = (precioEth * cantidadEth) /
            1000000000000000000;

        return cantidadEthEnUsd;
        // 0.00013187437091800
        // 0.00001318743709180
    }

    modifier onlyOwner() {
        require(msg.sender == duenoDelContrato);
        _;
    }

    function retiro() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);
        for (
            uint256 indiceFinanciadores = 0;
            indiceFinanciadores < financiadores.length;
            indiceFinanciadores++
        ) {
            address financiador = financiadores[indiceFinanciadores];
            direccionesQueDepositan[financiador] = 0;
        }
        // Esto vacia completamente al array
        financiadores = new address[](0);
    }

    // Traida de Github
    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = obtenerPrecio();
        uint256 precision = 1 * 10**18;
        // return (minimumUSD * precision) / price;
        // We fixed a rounding error found in the video by adding one!
        // return ((minimumUSD * precision) / price) + 1;
        return ((minimumUSD * precision) / price) + 1;
    }
}
