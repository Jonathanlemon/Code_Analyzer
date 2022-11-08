use XML::LibXML;
use strict;
use Data::Dumper;
use PDF::API2;
use FindBin;
use PDF::Table;
require "$FindBin::Bin/generateReportUtilities.pl";

#Command Line Arguments
# 0 = Differential XML location
# 1 = report location
# 2 = Settings different or not

#PDF setup
my $pdf = PDF::API2->new();
my $page;
my $content;
my $font = $pdf->corefont('Courier');

my $fontSize = 12;
my $marginSize = 40;
my $newLineHeight = $fontSize * 1.2;

#Variables for manipulating coordinate system for content
my $curX = $marginSize;
my $curY = 792 - $marginSize;

#Fault reporting variables
my $loopcount = 0;
my @pageHeaderArray = ("Errors:", "Warnings:", "Performance Issues:", "Portability Issues:", "Style Issues:", "Other:");
my $refNum = 0;
my $pageHeader = @pageHeaderArray[$loopcount];

#XML file handling
my $dom = XML::LibXML->load_xml(location => @ARGV[0]);

#Load Statistics
my @newBugs = $dom->findnodes('/results/new/error');
my @fixedBugs = $dom->findnodes('/results/fixed/error');

my @errorList;
my @warningList;
my @performanceList;
my @portabilityList;
my @styleList;
my @informationList;

#SRT Logo
my $logo = $pdf->image("$FindBin::Bin/resources/pdfHeader.jpg");

my %data = loadErrors(@newBugs);
my %anomalyHandler = %{$data{'anomalies'}};
my %idHandler = %{$data{"idStruct"}};

























                                                    #Function Definitions

#Function for creating new page
sub newPage{
    $page = $pdf->page();
    $page->mediabox('8.5x11');
    $content = $page->text();
    $content->font($font,$fontSize);

    $curX = $marginSize;
    $curY = 792 - $marginSize;

    $pageHeader = $pageHeaderArray[$loopcount];
    printFaultHeaderText();

    $content->fillcolor('#000000');
    $content->translate($curX,$curY);
}

#Print error type on top of page
sub printFaultHeaderText{
    $content->translate(306, 792-$fontSize-($marginSize/2));
    $content->text($pageHeader, (align => 'center'));
}

#Function for printing a line of errors
sub printLine{
    $content->translate($curX, $curY-$fontSize);
    my($text) = $_[0];
    my $remText = "";

    if($curY - ($fontSize) < $marginSize){
        newPage();
    }

    while($content->text_width($text) > (612 - $marginSize - $marginSize)){
        $remText = substr($text, length($text) - 1, 1).$remText;
        $text = substr($text, 0, length($text) - 1);
    }

    $content->text($text);
    
    $curY -= $newLineHeight;
    
    
    $content->translate($curX, $curY);
    
    if(length($remText) gt 0){
        printVerticalLines();
        printLine($remText);
    }
}


















sub printFormattedErrors{
    #Array to hold references to each fault array
    my @faultRefArray = ($anomalyHandler{"error"}, $anomalyHandler{"warning"}, $anomalyHandler{"performance"}, $anomalyHandler{"portability"}, $anomalyHandler{"style"}, $anomalyHandler{"information"}); 

    #Loop through each fault type array
    for my $ref (@faultRefArray){
        my $remainingData = "";
        #If there are faults for this type, create a new page
        if(scalar(@$ref) > 0){
            newPage();
        }
        #Loop through each fault in the respective fault type array, and load it into the printing buffer
        foreach(@$ref){
            $refNum++;

            my @linesToPrint;
            my @loc = $_->getElementsByTagName("location");
            my @symbol = $_->getElementsByTagName("symbol");
            my $msg = $_->getAttribute("msg");
            my $fileName = "";

            if(scalar @loc >= 1){
                $fileName = @loc[0]->getAttribute("file");
            }

            my $faultID = $_->getAttribute("id");
            my $faultHeader = substr($fileName, 34)." : [".$faultID."]";

            my $displayMessageInHeader = 1;

            #Only care about faults that are actually in source code
            if ($fileName ne "") {
                foreach(@loc){
                    #If the fault has a main location, use it for fault message instead of header
                    if(length($_->getAttribute("info")) == 0){
                        $displayMessageInHeader = 0;
                        last;
                    }
                }

                push(@linesToPrint, $faultHeader);

                if($displayMessageInHeader != 0){
                    push(@linesToPrint, $msg);
                }

                if(scalar @symbol >= 1){
                    push(@linesToPrint, "Anomaly found with: \"".$symbol[0]->textContent."\"");
                }

                push(@linesToPrint, "");

                open(my $f, '<', $fileName);
                my $linecount = 1;
                my $matchNum = 0;

                #Get lines from source code files
                while(<$f>){
                    chomp($_);

                    #Ensure all instances of the fault (multiple locations) are handled
                    foreach my $locInstance (@loc){
                        if($linecount == $locInstance->getAttribute("line")){

                            $matchNum++;
                            $remainingData = $remainingData.$locInstance->getAttribute("line").":".$locInstance->getAttribute("column")." - ";
                            if(length($locInstance->getAttribute("info")) > 0){
                                $remainingData = $remainingData."(".$locInstance->getAttribute("info").")\n";
                            }
                            else{
                                $remainingData = $remainingData.$msg;
                            }
                            push(@linesToPrint, $remainingData);
                            $remainingData = "";
                            #Replace tabs with ' '
                            while(index($_, "\t") >= 0){
                                $_ =~ s/\t/ /;
                            }

                            #Handles multi-line statements
                            my $charNum = $locInstance->getAttribute("column");
                            while((length($_) < $charNum) and (length($_) > 0)){
                                $charNum = $charNum - length($_);
                                $_ = <$f>;
                            }

                            #Handles highlighting fault location
                            chomp($_);
                            if($charNum < 30){
                                $remainingData = $remainingData.substr($_, 0, 70);
                                push(@linesToPrint, $remainingData);
                                $remainingData = "";
                                foreach(my $i = 0;$i < $charNum-1; $i++){
                                    $remainingData=$remainingData." ";
                                }
                            }
                            else{
                                $remainingData = $remainingData.substr($_, $charNum-30, 70);
                                push(@linesToPrint, $remainingData);
                                $remainingData = "                             ";
                            }
                            $remainingData=$remainingData."^";
                            push(@linesToPrint, $remainingData);
                            $remainingData = "";
                        }
                    }

                    #If all fault locations are handled, done with loop and can close file
                    if($matchNum >= @loc){
                        last;
                    }
                    $linecount++;
                }
                close($f);

                #Print box to page
                printGrouping(@linesToPrint);
                printLine("");
                printLine("");
                printLine("");
                printLine("");
            }
            else{
                #Even if the fault doesn't have a location (Ex: Information errors), still print it
                if($faultID eq "missingInclude"){
                    printGrouping("The analyzer detected missing include(s). Please ensure all of the project's include directories are also included in the analyzer settings.");
                }
                else{
                    printGrouping($msg);
                }
                printLine("");
                printLine("");
                printLine("");
                printLine("");
            }
        }

        #Increment when a classification of fault is finished
        $loopcount++;
    }
}














#Function for printing top and bottom lines of box
sub printHorizontalLine{
    if($loopcount eq 0){
        $content->stroke_color("red");
    }
    if($loopcount eq 1){
        $content->stroke_color("orange");
    }
    if($loopcount eq 2){
        $content->stroke_color("yellow");
    }
    if($loopcount eq 3){
        $content->stroke_color("green");
    }
    if($loopcount eq 4){
        $content->stroke_color("blue");
    }
    if($loopcount eq 5){
        $content->stroke_color("pink");
    }

    $content->translate($curX, $curY);
    $content->line_width(3);
    $content->rectangle($curX-3, $curY, 583, $curY);
    $content->stroke();
}

#Function for printing sides of box
sub printVerticalLines{
    if($loopcount eq 0){
        $content->stroke_color("red");
    }
    if($loopcount eq 1){
        $content->stroke_color("orange");
    }
    if($loopcount eq 2){
        $content->stroke_color("yellow");
    }
    if($loopcount eq 3){
        $content->stroke_color("green");
    }
    if($loopcount eq 4){
        $content->stroke_color("blue");
    }
    if($loopcount eq 5){
        $content->stroke_color("pink");
    }
    $content->translate($curX, $curY);
    $content->line_width(3);
    $content->rectangle($curX-3, $curY, $curX-3, $curY - $newLineHeight);
    $content->rectangle(583, $curY, 583, $curY - $newLineHeight);
    $content->stroke();
}

#Function to print a box with text inside
sub printGrouping{
    #Ensure the grouping can fit on the page
    my $calculatedHeight = 1;
    foreach my $line (@_){
        my $width = $content->text_width($line);
        while($width > (612 - $marginSize - $marginSize)){
            $calculatedHeight++;
            $width -= (612 - $marginSize - $marginSize);
        }
        $calculatedHeight++;
    }

    #If it can't make a new page
    if($curY - ($calculatedHeight * $newLineHeight) < $marginSize){
        newPage();
    }

    #Print to page
    printLine("#".$refNum);
    printHorizontalLine();
    foreach my $data (@_){
        if($curY - ($fontSize) < $marginSize){
            newPage();
        }
        printVerticalLines();
        printLine($data);
    }
    printHorizontalLine();
}



















#Title Page
my $header;

$page = $pdf->page();
$page->mediabox('8.5x11');
$content = $page->text();
$content->font($font,20);
$content->fillcolor('#000000'); 
$page->object($logo, 200, 700, 200);
$content->translate(300, 680);

#Title Page Header
$header = "Differential Scan Report";

#Timestamp and main stat
$header = $header."\n".localtime();
$header = $header."\n\n"."New Anomalies Detected: ".@newBugs;
$header = $header."\n\n"."Fixed Anomalies Detected: ".@fixedBugs;
$content->section($header, 400, 800, , (align => 'center'));

#Display Pie Chart
$content = $page->graphics();
drawPieChart(300, 480, 50, $content, scalar(@newBugs), %anomalyHandler);
$content = $page->text();

$header = "";
$content->font($font, 14);
$content->translate($marginSize, 400);

#TABLE DISPLAY OF SEVERITY AND ID TYPE
drawStatisticsTables($pdf, $page, \%anomalyHandler, \%idHandler, $marginSize, $font);


if(@ARGV[2] eq "SETTINGSDIFFERENT"){
    $content->fillcolor('#ff0000'); 
    $content->font($font, 14);
    $content->translate(300, 40);
    $content->text("Warning: Different analyzer settings were used between the two scans.", align=>'center'); 
    $content->transform(translate => [0, -17], relative => 1);
    $content->text("This may be responsible for altering differential scan results.", align=>'center'); 
}



















#Print Base Settings Page
$page = $pdf->page();
$page->mediabox('8.5x11');
$content = $page->text();
$content->font($font,14);
$content->fillcolor('#000000'); 
$page->object($logo, 40, 760, 100);
$content->translate($marginSize, 700);

my $pdftable = new PDF::Table;
$pdftable->table($pdf, $page, [["Base Scan Analyzer Settings"]], 'x' => $marginSize,'y' => 750, 'h' => 100, 'w' => 613-$marginSize-$marginSize,'font_size' => 14,'font' => $font,'justify' =>'center','max_word_length' => 70);

my @enableList = $dom->findnodes('/results/oldSettings/settings/enables');
my @includeList = $dom->findnodes('/results/oldSettings/settings/includes');
my @excludeList = $dom->findnodes('/results/oldSettings/settings/excludes');
my @suppressionList = $dom->findnodes('/results/oldSettings/settings/suppressions');
my @definesList = $dom->findnodes('/results/oldSettings/settings/defines');
my @targetList = $dom->findnodes('/results/oldTargets/targets/target');


my $settingsContent = "Target(s):\n";
foreach(@targetList){
    $settingsContent = $settingsContent.substr($_->getAttribute("value"), -70)."\n";
}

$settingsContent = $settingsContent."\nEnabled Checks:\nerrors\n";
foreach(@enableList){
    $settingsContent = $settingsContent.$_->getAttribute("value")."\n";
}

if(scalar(@includeList) > 0){
    $settingsContent = $settingsContent."\nInclude Paths:\n";
    foreach(@includeList){
        $settingsContent = $settingsContent.substr($_->getAttribute("value"), -70)."\n";
    }
}

if(scalar(@excludeList) > 0){
    $settingsContent = $settingsContent."\nExclude Paths:\n";
    foreach(@excludeList){
        $settingsContent = $settingsContent.substr($_->getAttribute("value"), -70)."\n";
    }
}

if(scalar(@suppressionList) > 0){
    $settingsContent = $settingsContent."\nSuppressions:\n";
    foreach(@suppressionList){
        $settingsContent = $settingsContent.$_->getAttribute("value")."\n";
    }
}

if(scalar(@definesList) > 0){
    $settingsContent = $settingsContent."\nPreprocessor Definitions:\n";
    foreach(@definesList){
        $settingsContent = $settingsContent.$_->getAttribute("value")."\n";
    }
}

my $remainingText = $content->section($settingsContent, 550, 650, , (align => 'left'));


while(length($remainingText) > 0){
    $page = $pdf->page();
    $page->mediabox('8.5x11');
    $content = $page->text();
    $content->font($font,14);
    $content->fillcolor('#000000'); 
    $page->object($logo, 40, 760, 100);

    $content->translate($marginSize, 700);

    $remainingText = $content->section($remainingText, 550, 650, , (align => 'left'));
}












#Print Current Settings Page
$page = $pdf->page();
$page->mediabox('8.5x11');
$content = $page->text();
$content->font($font,14);
$content->fillcolor('#000000'); 
$page->object($logo, 40, 760, 100);
$content->translate($marginSize, 700);

my $pdftable = new PDF::Table;
$pdftable->table($pdf, $page, [["Current Scan Analyzer Settings"]], 'x' => $marginSize,'y' => 750, 'h' => 100, 'w' => 613-$marginSize-$marginSize,'font_size' => 14,'font' => $font,'justify' =>'center','max_word_length' => 70);

my @enableList = $dom->findnodes('/results/newSettings/settings/enables');
my @includeList = $dom->findnodes('/results/newSettings/settings/includes');
my @excludeList = $dom->findnodes('/results/newSettings/settings/excludes');
my @suppressionList = $dom->findnodes('/results/newSettings/settings/suppressions');
my @definesList = $dom->findnodes('/results/newSettings/settings/defines');
my @targetList = $dom->findnodes('/results/newTargets/targets/target');

$settingsContent = "Target(s):\n";
foreach(@targetList){
    $settingsContent = $settingsContent.substr($_->getAttribute("value"), -70)."\n";
}


$settingsContent = $settingsContent."\nEnabled Checks:\nerrors\n";
foreach(@enableList){
    $settingsContent = $settingsContent.$_->getAttribute("value")."\n";
}

if(scalar(@includeList) > 0){
    $settingsContent = $settingsContent."\nInclude Paths:\n";
    foreach(@includeList){
        $settingsContent = $settingsContent.substr($_->getAttribute("value"), -70)."\n";
    }
}

if(scalar(@excludeList) > 0){
    $settingsContent = $settingsContent."\nExclude Paths:\n";
    foreach(@excludeList){
        $settingsContent = $settingsContent.substr($_->getAttribute("value"), -70)."\n";
    }
}

if(scalar(@suppressionList) > 0){
    $settingsContent = $settingsContent."\nSuppressions:\n";
    foreach(@suppressionList){
        $settingsContent = $settingsContent.$_->getAttribute("value")."\n";
    }
}

if(scalar(@definesList) > 0){
    $settingsContent = $settingsContent."\nPreprocessor Definitions:\n";
    foreach(@definesList){
        $settingsContent = $settingsContent.$_->getAttribute("value")."\n";
    }
}

my $remainingText = $content->section($settingsContent, 550, 650, , (align => 'left'));


while(length($remainingText) > 0){
    $page = $pdf->page();
    $page->mediabox('8.5x11');
    $content = $page->text();
    $content->font($font,14);
    $content->fillcolor('#000000'); 
    $page->object($logo, 40, 760, 100);

    $content->translate($marginSize, 700);

    $remainingText = $content->section($remainingText, 550, 650, , (align => 'left'));
}











#Print New Anomalies first
printFormattedErrors();

#Then print "fixed" bugs aka bugs that were in the old scan but not found in the new scan

$loopcount = 0;
my %data = loadErrors(@fixedBugs);
my %anomalyHandler = %{$data{'anomalies'}};
my %idHandler = %{$data{"idStruct"}};


#Print fixed anomalies next
#Array to hold references to each fault array
my @faultRefArray = ($anomalyHandler{"error"}, $anomalyHandler{"warning"}, $anomalyHandler{"performance"}, $anomalyHandler{"portability"}, $anomalyHandler{"style"}, $anomalyHandler{"information"}); 

#Loop through each fault type array
for my $ref (@faultRefArray){
    my $remainingData = "";
    #If there are faults for this type, create a new page
    if(scalar(@$ref) > 0){
        newPage();
    }
    #Loop through each fault in the respective fault type array, and load it into the printing buffer
    foreach(@$ref){
        $refNum++;

        my @linesToPrint;
        my @loc = $_->getElementsByTagName("location");
        my @symbol = $_->getElementsByTagName("symbol");
        my $msg = $_->getAttribute("msg");
        my $fileName = "";

        if(scalar @loc >= 1){
            $fileName = @loc[0]->getAttribute("file");
        }

        my $faultID = $_->getAttribute("id");
        my $faultHeader = substr($fileName, 34)." : [".$faultID."]";

        my $displayMessageInHeader = 1;

        #Only care about faults that are actually in source code
        if ($fileName ne "") {
            foreach(@loc){
                #If the fault has a main location, use it for fault message instead of header
                if(length($_->getAttribute("info")) == 0){
                    $displayMessageInHeader = 0;
                    last;
                }
            }

            push(@linesToPrint, "Fixed:");
            push(@linesToPrint, " ");
            push(@linesToPrint, $faultHeader);

            if($displayMessageInHeader != 0){
                push(@linesToPrint, $msg);
            }

            if(scalar @symbol >= 1){
                push(@linesToPrint, "Anomaly found with: \"".$symbol[0]->textContent."\"");
            }

            foreach my $locInstance (@loc){
                    $remainingData = $remainingData.$locInstance->getAttribute("line").":".$locInstance->getAttribute("column")." - ";
                    if(length($locInstance->getAttribute("info")) > 0){
                        $remainingData = $remainingData."(".$locInstance->getAttribute("info").")\n";
                    }
                    else{
                        $remainingData = $remainingData.$msg;
                    }
                    push(@linesToPrint, $remainingData);

                    $remainingData = "";
            }

            #Print box to page
            printGrouping(@linesToPrint);
            printLine("");
            printLine("");
            printLine("");
            printLine("");
        }
        else{
            #Even if the fault doesn't have a location (Ex: Information errors), still print it
            if($faultID eq "missingInclude"){
                printGrouping("The analyzer detected missing include(s). Please ensure all of the project's include directories are also included in the analyzer settings.");
            }
            else{
                printGrouping($msg);
            }
            printLine("");
            printLine("");
            printLine("");
            printLine("");
        }
    }

    #Increment when a classification of fault is finished
    $loopcount++;
}




$pdf->saveas(@ARGV[1]);
