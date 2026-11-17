// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StudentRegistry {
    struct Student {
        uint256 rollNo;
        string name;
        string department;
    }

    Student[] private students;
    mapping(uint256 => bool) private usedRollNo;
    address public immutable owner;

    event StudentAdded(uint256 indexed rollNo, string name);
    event FallbackCalled(address indexed sender, bytes data);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    function addStudent(
        uint256 rollNo,
        string calldata name,
        string calldata department
    ) external onlyOwner {
        require(rollNo > 0, "Invalid roll number");
        require(!usedRollNo[rollNo], "Duplicate roll number");
        require(bytes(name).length > 0, "Name required");
        require(bytes(department).length > 0, "Department required");

        usedRollNo[rollNo] = true;
        students.push(Student(rollNo, name, department));
        emit StudentAdded(rollNo, name);
    }

    function getStudent(uint256 index)
        external
        view
        returns (uint256, string memory, string memory)
    {
        require(index < students.length, "Index out of range");
        Student storage student = students[index];
        return (
            student.rollNo, student.name, student.department
        );
    }

    function studentCount() external view returns (uint256) {
        return students.length;
    }

    fallback() external {
        emit FallbackCalled(msg.sender, msg.data);
    }
}
