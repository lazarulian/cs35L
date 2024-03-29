# Compression

## Table of Contents

- [Compression](#compression)
  - [Table of Contents](#table-of-contents)
  - [Huffman Coding](#huffman-coding)
    - [Decompressing](#decompressing)
    - [Table Generation Algorithm](#table-generation-algorithm)
  - [Dictionary Compression](#dictionary-compression)
    - [Adaptive Dictionary Compression (Sliding Window)](#adaptive-dictionary-compression-sliding-window)
    - [Huffman Encoding vs. Dictionary Compression](#huffman-encoding-vs-dictionary-compression)
  - [Z-Lib](#z-lib)
    - [Compression Downsides](#compression-downsides)

## Huffman Coding

The best possible algorithm under its constraints:

1. Input is a sequence of symbols taken from a known alphabet.
2. We know the _popularity_ of each input symbol.
3. Each input symbol corresponds to some bit stream.

When you have these constraints, you can assemble a table mapping input symbols to output bit strings, with lengths chosen based on how frequent they are. With ASCII characters in the context of the English language as an example:

| Symbol  | Bit String   |
| ------- | ------------ |
| (space) | 00           |
| e       | 010          |
| t       | 011          |
| a       | 100          |
| o       | 1010         |
| ...     | ...          |
| ^Q      | 111011011101 |

- Notice that the least popular symbols could map to a representation that takes up even more space than their original form, but that's okay because they occur so scarcely that on average it does not hinder the total length by much.
- Characters that occur more frequently are assigned shorter binary codes, while characters that occur less frequently are assigned longer binary codes.
- compression is simply a matter of iterating over the input symbols and performing a lookup.

### Decompressing

- **OPTION A:** You have a pre-computed table shared by the compressor and de-compressor. Sender computes the table and sends it first. This introduces some overhead in transmission, but more importantly, it has to read all of the input first.

- **OPTION B: Dynamic Hoffman tables**.

  1.  Both sender and recipient start off with a table in their head that's perfectly balanced (for example, every character standing for itself).
  2.  Sender then sends the first byte and updates its Hoffman table according to the byte that it already sent.
  3.  The recipient does the same, and because both sides can detect the same popularity of the data they are sending/receiving, their tables are kept in sync.

  This is a little slower because they have to update the tables dynamically as they go but not by much. You also have to agree on what to do when there's a tie in popularity. Both sides need to be able to stay in lock step with each other.

### Table Generation Algorithm

Suppose you computed a table of probabilities (possibly by counting the frequencies of each symbol in some sample text):

| Symbol   | Probability |
| -------- | ----------- |
| (space)  | 0.1         |
| e        | 0.07        |
| t        | 0.05        |
| ...      | ...         |
| **SUM:** | 1.0         |

You build a **Huffman tree** to determine the bit string to assign. Review your MATH 61 notes lol.

## Dictionary Compression

- The sender and the recipient both maintain a dictionary of words
- you have a numbered dictionary that associates a number with each word
  - over the internet, you send the numbers rather than the words themselves to save space over the internet
  - with larger dictionaries you can use a different number of bytes to store these values
- This is really a dictionary of byte strings, so `hello,` can be a word

### Adaptive Dictionary Compression (Sliding Window)

---

- the sender will send some data with an empty dictionary
- when the sender starts sending some things to the recipient, then they start building up the dictionary
  - often, there is a construction algorithm that builds up the dictionary before sending the codes
  - some downsides are that size can be an issue when the messages can be very large
- to ensure the dictionary does not grow in size too large, we can use a dictionary window that adds and discards words from the dictionary
  - The basic idea of the sliding window technique is to maintain a sliding window of a 64kb over the input data.
  - The window starts at the beginning of the input stream and slides over the data as more data is read.
    - The sliding window can be visualized as a fixed-size buffer that contains the last N bytes of the input stream, where N is the size of the window.

> For example, suppose the input data is "ABCABCABCDEFDEF" and the sliding window size is 9 bytes. When the compressor encounters the second occurrence of the pattern "ABC", it replaces it with a reference to the previous occurrence of the same pattern within the sliding window. The reference consists of the distance (which is 3, since the previous occurrence is three bytes back in the window) and the length (which is 3, since the pattern "ABC" is three bytes long).

- When the compressor encounters a repeating pattern in the input data, it replaces the repeated pattern with a reference to the previous occurrence of the same pattern within the sliding window.
  - This reference is typically represented by two values: the distance to the previous occurrence of the pattern (i.e., the number of bytes between the current position and the previous occurrence), and the length of the repeated pattern
- good dictionaries implement a hash table of the words allowing for the efficiency of o(log(w))

### Huffman Encoding vs. Dictionary Compression

- dictionary compression is a better approach than huffman encoding because it is byte-byte encoding rather than actual compression/encoding
  - with dictionary compression, you really compress well if repeated strings are within the dictionaries between the sender and the recipient
  - One of the main advantages of dictionary encoding over Huffman encoding is that it can achieve a higher compression ratio since it uses a fixed-length code for each entry in the dictionary, and therefore can be more efficient for data that has a repetitive structure.
  - However, the downside of dictionary encoding is that it requires the dictionary to be included in the compressed data, which adds overhead to the compressed file size. This can make dictionary encoding less effective for data with a high degree of randomness or where the dictionary is large.
- Huffman encoding is suitable for data with a variable frequency distribution of characters, while dictionary encoding is more suitable for data with a repetitive structure or pattern.
  - The choice between the two techniques depends on the specific characteristics of the data being compressed and the trade-off between compression ratio and overhead.

## Z-Lib

- Z-Lib uses both Huffman Encoding and Adaptive Dictionary Compression
  - Zlib implements an optimized version of LZ77 known as LZ77-2, which uses a sliding window technique to keep track of the last 32 kilobytes of input data.
  - After applying the LZ77 compression, Zlib uses Huffman coding to further compress the output.
- Huffman coding assigns shorter codes to frequently occurring patterns and longer codes to less frequently occurring patterns.
  - results in a more efficient compression of the data, especially for data with a non-uniform frequency distribution of patterns
  - You get a bit string that represents the string of symbols but shorter

### Compression Downsides

- Consider you have a compressed data and one of the blocks is corrupted
- If there is one bad block, it ruins the rest of the data. There is a greater strain on the underlying system, such that everything must be reliable when using compression
