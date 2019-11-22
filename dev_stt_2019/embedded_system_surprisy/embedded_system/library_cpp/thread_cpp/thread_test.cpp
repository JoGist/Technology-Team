#include <iostream>
#include <thread>

class Task
{
public:
	void execute(std::string command)
	{
		for(int i = 0; i < 5; i++)
		{
			std::cout<<command<<" :: "<<i<<std::endl;
		}
	}

};

int main()
{
	Task * taskPtr = new Task();

	// Create a thread using member function
	std::thread th(&Task::execute, taskPtr, "Sample Task");

	th.join();

	delete taskPtr;
	return 0;
}


// g++ -std=c++0x thread_test.cpp -o thread_test -lpthread
