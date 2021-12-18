#include "MatlabEngine.hpp"
#include "MatlabDataArray.hpp"
#include "iostream"
#include <vector>
#include <string>
using namespace std;


void findNConnect() {
    using namespace matlab::engine;

    // Find and connect to shared MATLAB session
    std::unique_ptr<MATLABEngine> matlabPtr;
    std::vector<String> names = findMATLAB();
    std::vector<String>::iterator it;
    it = std::find(names.begin(), names.end(), u"myMatlabEngine");
    if (it != names.end()) {
        matlabPtr = connectMATLAB(*it);
    }

    // Determine if engine connected
    if (matlabPtr){
        matlab::data::ArrayFactory factory;
        matlab::data::CharArray arg = factory.createCharArray("-release");
        matlab::data::CharArray version = matlabPtr->feval(u"version", arg);
        std::cout << "Connected to: " << version.toAscii() << std::endl;
    }
    else {
        std::cout << "myMatlabEngine not found" << std::endl;
    }
}

int main() {
    findNConnect();

    return 0;
}