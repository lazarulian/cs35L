import React from "react";
import { useState } from "react";

function calculateWinner(squares) {
  // Function that Determines whether the game has been won
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

function validMove(first, second, squares) {
  // Function that determines whether the move is valid or not after the tic-tac-toe portion has ended
  const first_i = Math.floor(first / 3);
  const first_j = first % 3;
  const second_i = Math.floor(second / 3);
  const second_j = second % 3;

  if (
    first_i - second_i <= 1 &&
    first_i - second_i >= -1 &&
    first_j - second_j <= 1 &&
    first_j - second_j >= -1
  ) {
    if (squares[second] === null) {
      return true;
    }
  }
  return false;
}

function Square({ value, onSquareClick }) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}

export default function Board() {
  const [xIsNext, setXIsNext] = useState(true);
  const [squares, setSquares] = useState(Array(9).fill(null));
  const [counter, setCounter] = useState(0);
  const [isFirstClick, setIsFirstClick] = useState(true);
  const [previousClick, setPreviousClick] = useState(-1);

  function handleClick(i) {
    // Handles the Click of when a player tries to make a move on the board
    const nextSquares = squares.slice();
    if (counter < 6) {
      if (calculateWinner(squares) || squares[i]) {
        return;
      }
      nextSquares[i] = xIsNext ? "X" : "O";
      setSquares(nextSquares);
      setXIsNext(!xIsNext);
      setCounter(counter + 1);
    } else {
      if (isFirstClick) {
        if (
          !nextSquares[i] ||
          calculateWinner(squares) ||
          (nextSquares[i] === "O" && xIsNext) ||
          (nextSquares[i] === "X" && !xIsNext)
        ) {
          return;
        }
        setPreviousClick(i);
        setIsFirstClick(!isFirstClick);
      } else {
        if (validMove(previousClick, i, nextSquares)) {
          if (
            nextSquares[4] === null ||
            nextSquares[4] === (xIsNext ? "O" : "X") ||
            previousClick === 4
          ) {
            nextSquares[i] = xIsNext ? "X" : "O";
            nextSquares[previousClick] = null;

            setSquares(nextSquares);
            setXIsNext(!xIsNext);
            setIsFirstClick(!isFirstClick);
          } else {
            nextSquares[i] = xIsNext ? "X" : "O";
            nextSquares[previousClick] = null;
            if (calculateWinner(nextSquares)) {
              setSquares(nextSquares);
              return;
            } else {
              setIsFirstClick(!isFirstClick);
            }
          }
        } else {
          setIsFirstClick(!isFirstClick);
          return;
        }
      }
    }
  }

  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = "Winner: " + winner;
  } else {
    status = "Next player: " + (xIsNext ? "X" : "O");
  }

  return (
    <div>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </div>
  );
}
