#include <cstdlib>
#include <iostream>
#include <map>
#include <fastcgi++/manager.hpp>
#include <fastcgi++/request.hpp>

class TestRequest : public Fastcgipp::Request<char> {
public:
    TestRequest() : Fastcgipp::Request<char>(1024) {}
private:
    bool response() {
        return true;
    }
};

int main(void) {
    Fastcgipp::Manager<TestRequest> manager;

    const char input[] = "test1=test&test2=test&";

    std::multimap<std::string, std::string> output;
    Fastcgipp::Http::decodeUrlEncoded(
        std::begin(input),
        std::end(input),
        output);

    for (const auto& [key, value] : output) {
        std::cout << key << " -> " << value << "\n";
    }

    return EXIT_SUCCESS;
}
