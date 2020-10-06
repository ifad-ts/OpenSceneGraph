#include <osg/ArgumentParser>

int main( int argc, char** argv )
{
    osg::ArgumentParser arguments(&argc,argv);

    arguments.getApplicationUsage()->setDescription(arguments.getApplicationName()+" is the example which runs units tests.");
    arguments.getApplicationUsage()->setCommandLineUsage(arguments.getApplicationName()+" [options]");
    arguments.getApplicationUsage()->addCommandLineOption("-h or --help","Display this information");
	
	return 0;
}