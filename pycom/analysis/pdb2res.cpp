#include <bits/stdc++.h>
#include <zlib.h>

/**
 * Authored by Philipp Bibik (cemiu).
 * 
 * Script for extracting residues alongside coordinates from PDB files.
 *
 * Compile with -lz option for zLib:
 *     g++ -std=c++17 pdb2res.cpp -lz -o pdb2res
 *
 * Input:
 *     line-seperated list of *.ent.gz file paths in the following format. e.g.:
 *         pdb/oy/pdb3oyz.ent.gz
 *.        pdb_files/pdb4f7r.ent.gz
 * Output:
 *     line-seperated list residues with AA, sequence number, and coordinates
 *     <amino_acid_code> <sequence_no> <x> <y> <y>
 *     Missing residues are denoted by a '.' (dot) character, and 'nan' coordinates
 *     Output is 0-indexed, and padded with n missing residues if first n residues are missing
 *     e.g.:
 *     . 0 nan nan nan
 *     . 1 nan nan nan
 *     R 4 -13.945 -18.12 61.032
 *     H 5 -17.627 -18.063 57.517
 */

using namespace std;

const std::unordered_map<std::string, char> aminoAcidLookup = {
    {"ALA", 'A'}, {"ARG", 'R'}, {"ASN", 'N'}, {"ASP", 'D'},
    {"CYS", 'C'}, {"GLN", 'Q'}, {"GLU", 'E'}, {"GLY", 'G'},
    {"HIS", 'H'}, {"HIP", 'H'}, {"HIE", 'H'}, {"ILE", 'I'},
    {"LEU", 'L'}, {"LYS", 'K'}, {"MET", 'M'}, {"PHE", 'F'},
    {"PRO", 'P'}, {"SER", 'S'}, {"THR", 'T'}, {"TYR", 'Y'},
    {"TRP", 'W'}, {"VAL", 'V'}, // {"SEC", 'U'}, {"PYL", 'O'}, // selenocysteine & pyrrolysine
};

std::stringstream decompressGZFile(const std::string& filename) {
    gzFile gzfile = gzopen(filename.c_str(), "rb");
    if (!gzfile) {
        std::cerr << "Failed to open file " << filename << std::endl;
        return std::stringstream();
    }

    char buffer[4096];
    std::stringstream ss;
    int num_read = 0;
    while ((num_read = gzread(gzfile, buffer, sizeof(buffer))) > 0) {
        ss.write(buffer, num_read);
    }

    gzclose(gzfile);
    return ss;
}

void print_sequence_from_pdb(std::stringstream& pdb) {
    vector<pair<int, char>> v;
    int last_res = 0;

    string line;
    while(std::getline(pdb, line)) {
        string statement = line.substr(0, 4); // "ATOM" || "TER "
        if (statement == "TER ") break; // first strand over
        if (statement != "ATOM") continue; // ignore non-atom statements

        string atom = line.substr(13, 2);
        if (atom != "CA" && atom != "CB") continue; // only consider C_a or C_b atoms
        string aa = line.substr(17, 3);
        if (atom == "CA" && aa != "GLY") continue; // only consider C_a for glycine
        if (aminoAcidLookup.find(aa) == aminoAcidLookup.end()) continue; // not standard AA

        char aa_s = aminoAcidLookup.at(aa);
        int resseq = stoi(line.substr(23, 4));

        v.push_back(make_pair(resseq, aa_s));

        float x = stof(line.substr(30, 8));
        float y = stof(line.substr(38, 8));
        float z = stof(line.substr(46, 8));

        // pad sequence when residues are missing
        // Format: ". <seq_no> nan nan nan"
        for (int i = last_res+1; i<resseq; i++) {
            cout << ". " << i - 1 << " nan nan nan" << endl;
        }
        last_res = resseq;

         cout << aa_s << " " << resseq - 1 << " " << x << " " << y << " " << z << endl;
    }
}

int main() {
    ios_base::sync_with_stdio(false); cin.tie(NULL);

    vector<string> files;
    string next_file;
    while (getline(cin, next_file)) {
        files.push_back(next_file);
    }

    // cout << files[0] << endl;

    for (auto file : files) {
        auto pdb_ss = decompressGZFile(file);
        print_sequence_from_pdb(pdb_ss);
        stringstream().swap(pdb_ss);
    }

    return 0;
}
