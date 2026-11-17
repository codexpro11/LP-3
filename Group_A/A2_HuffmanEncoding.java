import java.util.*;

/**
 * Group A - Assignment No: 2
 * Title: Write a program to implement Huffman Encoding using a greedy strategy.
 */
public class A2_HuffmanEncoding {

    public static class HuffmanNode implements Comparable<HuffmanNode> {
        public Character ch; // null for internal nodes
        public int freq;
        public HuffmanNode left;
        public HuffmanNode right;
        public boolean isLeaf;
        public int creationOrder;

        public HuffmanNode(Character ch, int freq, int creationOrder) {
            this.ch = ch;
            this.freq = freq;
            this.left = null;
            this.right = null;
            this.isLeaf = (ch != null);
            this.creationOrder = creationOrder;
        }

        public HuffmanNode(int freq, HuffmanNode left, HuffmanNode right, int creationOrder) {
            this.ch = null;
            this.freq = freq;
            this.left = left;
            this.right = right;
            this.isLeaf = false;
            this.creationOrder = creationOrder;
        }

        @Override
        public int compareTo(HuffmanNode other) {
            if (this.freq != other.freq) {
                return Integer.compare(this.freq, other.freq);
            }
            // For identical frequencies, internal nodes take precedence over leaves,
            // matching standard manual tie-breaking order in course materials.
            if (this.isLeaf != other.isLeaf) {
                return this.isLeaf ? 1 : -1;
            }
            return Integer.compare(this.creationOrder, other.creationOrder);
        }
    }

    public static HuffmanNode buildHuffmanTree(Map<Character, Integer> freqMap) {
        if (freqMap == null || freqMap.isEmpty()) {
            return null;
        }

        PriorityQueue<HuffmanNode> pq = new PriorityQueue<>();
        int orderCounter = 0;
        for (Map.Entry<Character, Integer> entry : freqMap.entrySet()) {
            pq.add(new HuffmanNode(entry.getKey(), entry.getValue(), orderCounter++));
        }

        // Special case: only 1 distinct character
        if (pq.size() == 1) {
            HuffmanNode only = pq.poll();
            HuffmanNode root = new HuffmanNode(only.freq, only, null, orderCounter++);
            return root;
        }

        while (pq.size() > 1) {
            HuffmanNode left = pq.poll();
            HuffmanNode right = pq.poll();
            HuffmanNode parent = new HuffmanNode(left.freq + right.freq, left, right, orderCounter++);
            pq.add(parent);
        }

        return pq.peek();
    }

    public static void generateCodes(HuffmanNode node, String prefix, Map<Character, String> codeMap) {
        if (node == null) return;

        if (node.isLeaf) {
            codeMap.put(node.ch, prefix.isEmpty() ? "0" : prefix);
            return;
        }

        generateCodes(node.left, prefix + "0", codeMap);
        generateCodes(node.right, prefix + "1", codeMap);
    }

    public static String encode(String text, Map<Character, String> codeMap) {
        StringBuilder encoded = new StringBuilder();
        for (char c : text.toCharArray()) {
            encoded.append(codeMap.get(c));
        }
        return encoded.toString();
    }

    public static String decode(String bitString, HuffmanNode root) {
        if (root == null || bitString == null || bitString.isEmpty()) {
            return "";
        }

        // If single distinct character tree
        if (root.left != null && root.right == null && root.left.isLeaf) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < bitString.length(); i++) {
                sb.append(root.left.ch);
            }
            return sb.toString();
        }

        StringBuilder decoded = new StringBuilder();
        HuffmanNode curr = root;
        for (int i = 0; i < bitString.length(); i++) {
            char bit = bitString.charAt(i);
            curr = (bit == '0') ? curr.left : curr.right;

            if (curr != null && curr.isLeaf) {
                decoded.append(curr.ch);
                curr = root;
            }
        }
        return decoded.toString();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("=== Huffman Encoding (Greedy Strategy) ===");
        System.out.println("Choose Input Mode:");
        System.out.println("  1. Enter text string (e.g. BCAADDDCCACACAC)");
        System.out.println("  2. Enter character-frequency table (e.g. a:10, e:15, ...)");
        System.out.print("Enter choice (1 or 2) or paste string directly: ");

        if (!scanner.hasNextLine()) return;
        String line = scanner.nextLine().trim();
        while (line.isEmpty() && scanner.hasNextLine()) {
            line = scanner.nextLine().trim();
        }

        Map<Character, Integer> freqMap = new LinkedHashMap<>();
        String inputString = null;

        if (line.equals("1")) {
            System.out.print("Enter string to encode: ");
            inputString = scanner.nextLine().trim();
            for (char c : inputString.toCharArray()) {
                freqMap.put(c, freqMap.getOrDefault(c, 0) + 1);
            }
        } else if (line.equals("2")) {
            System.out.print("Enter number of distinct characters: ");
            int n = scanner.nextInt();
            scanner.nextLine();
            System.out.println("Enter each character and frequency (e.g., 'a 10' or 'a:10'):");
            for (int i = 0; i < n; i++) {
                System.out.print("Character " + (i + 1) + ": ");
                String row = scanner.nextLine().trim();
                while (row.isEmpty() && scanner.hasNextLine()) {
                    row = scanner.nextLine().trim();
                }
                String[] parts = row.replace(":", " ").split("\\s+");
                char c = parts[0].charAt(0);
                int f = Integer.parseInt(parts[1]);
                freqMap.put(c, f);
            }
        } else {
            // User pasted text string directly
            inputString = line;
            for (char c : inputString.toCharArray()) {
                freqMap.put(c, freqMap.getOrDefault(c, 0) + 1);
            }
        }

        if (freqMap.isEmpty()) {
            System.out.println("No characters to encode.");
            return;
        }

        // Build Huffman Tree
        HuffmanNode root = buildHuffmanTree(freqMap);

        // Generate Prefix Codes
        Map<Character, String> codeMap = new LinkedHashMap<>();
        generateCodes(root, "", codeMap);

        // Display results table
        System.out.println("\n-------------------------------------------------------------");
        System.out.printf("%-12s %-12s %-15s %-12s%n", "Character", "Frequency", "Huffman Code", "Bits (Freq*Len)");
        System.out.println("-------------------------------------------------------------");

        int totalFrequency = 0;
        int totalEncodedBits = 0;
        for (Map.Entry<Character, Integer> entry : freqMap.entrySet()) {
            char c = entry.getKey();
            int freq = entry.getValue();
            String code = codeMap.get(c);
            int bits = freq * code.length();

            totalFrequency += freq;
            totalEncodedBits += bits;

            System.out.printf("%-12s %-12d %-15s %-12d%n", "'" + c + "'", freq, code, bits);
        }
        System.out.println("-------------------------------------------------------------");

        double avgCodeLength = (double) totalEncodedBits / totalFrequency;
        int uncompressedBits = totalFrequency * 8; // standard 8-bit ASCII

        System.out.println("Total characters in message        : " + totalFrequency);
        System.out.println("Length of encoded message (in bits): " + totalEncodedBits + " bits");
        System.out.printf(Locale.US, "Average code length                : %.3f bits/character%n", avgCodeLength);
        System.out.println("Original uncompressed size (ASCII) : " + uncompressedBits + " bits (" + (totalFrequency) + " bytes)");
        double savings = (1.0 - ((double) totalEncodedBits / uncompressedBits)) * 100.0;
        System.out.printf(Locale.US, "Storage space saved                : %.2f%%%n", savings);

        // If full input string is available, encode and decode it
        if (inputString != null) {
            String encodedString = encode(inputString, codeMap);
            String decodedString = decode(encodedString, root);

            System.out.println("\nEncoded Bitstring:");
            System.out.println(encodedString);

            System.out.println("\nDecoded String (Verification):");
            System.out.println(decodedString);
            System.out.println("Lossless reconstruction: " + (inputString.equals(decodedString) ? "PASSED (Exact match)" : "FAILED"));
        }
    }
}
