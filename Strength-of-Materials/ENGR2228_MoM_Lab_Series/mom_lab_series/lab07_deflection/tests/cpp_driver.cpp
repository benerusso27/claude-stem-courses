// Reference driver for Lab 7: runs the instructor's beam_deflection.cpp solver (unchanged, included below with its
// main() renamed) on beams read from stdin, and prints the nodal results as JSON for tests/test_lab07_model.js.
//
//   g++ -std=c++17 -O2 -o cpp_driver cpp_driver.cpp      (from lab07_deflection/tests/)
//
// Input, one beam per block:   L E I nElem
//                              nSupports   then  type(P|R|F) x            per line
//                              nLoads      then  type(P|C|D) a b q1 q2    per line
// Units and signs are the C++ program's own: y DOWN positive, loads down positive, couples clockwise positive.
#define main beam_explorer_main
#include "../reference/beam_deflection.cpp"
#undef main

int main() {
    double L, E, I;
    int nElem;
    bool first = true;
    std::cout << "[";
    while (std::cin >> L >> E >> I >> nElem) {
        Beam bm;
        bm.L = L; bm.E = E; bm.I = I;
        int ns; std::cin >> ns;
        for (int i = 0; i < ns; ++i) {
            char t; double x; std::cin >> t >> x;
            bm.supports.push_back({t == 'F' ? FIX : t == 'P' ? PIN : ROL, x});
        }
        int nl; std::cin >> nl;
        for (int i = 0; i < nl; ++i) {
            char t; double a, b, q1, q2; std::cin >> t >> a >> b >> q1 >> q2;
            if (t == 'P') bm.loads.push_back(pointLoad(q1, a));
            else if (t == 'C') bm.loads.push_back(coupleLoad(q1, a));
            else bm.loads.push_back(distLoad(q1, q2, a, b));
        }
        const Solution sol = solveBeam(bm, nElem);
        std::cout << (first ? "" : ",") << "{\"ok\":" << (sol.ok ? "true" : "false") << ",\"x\":[";
        first = false;
        std::cout << std::setprecision(17);
        for (size_t i = 0; i < sol.xn.size(); ++i) std::cout << (i ? "," : "") << sol.xn[i];
        std::cout << "],\"y\":[";
        for (size_t i = 0; i < sol.yn.size(); ++i) std::cout << (i ? "," : "") << sol.yn[i];
        std::cout << "],\"t\":[";
        for (size_t i = 0; i < sol.tn.size(); ++i) std::cout << (i ? "," : "") << sol.tn[i];
        std::cout << "],\"R\":[";
        for (size_t i = 0; i < sol.reactions.size(); ++i)
            std::cout << (i ? "," : "") << "[" << sol.reactions[i].x << "," << sol.reactions[i].F_up << "," << sol.reactions[i].M_cw << "]";
        std::cout << "]}";
    }
    std::cout << "]\n";
    return 0;
}
