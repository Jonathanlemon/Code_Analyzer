
sub loadErrors{
    my @allErrors = @_;

    my (@errorList, @warningList, @performanceList, @styleList, @portabilityList, @informationList);

    my %errorID;
    my %warningID;
    my %performanceID;
    my %portabilityID;
    my %styleID;
    my %informationID;

    my %anomalies;
    my %idStruct;

    my %returnValue;

    #Load Errors into statistics
    foreach my $issue (@allErrors){
        if ($issue->getAttribute("severity") eq "error"){
            push(@errorList, $issue);
            $errorID{$issue->getAttribute("id")} = $errorID{$issue->getAttribute("id")} + 1;
        }
        elsif ($issue->getAttribute("severity") eq "warning"){
            push(@warningList, $issue);
            $warningID{$issue->getAttribute("id")} = $warningID{$issue->getAttribute("id")} + 1;
        }
        elsif ($issue->getAttribute("severity") eq "performance"){
            push(@performanceList, $issue);
            $performanceID{$issue->getAttribute("id")} = $performanceID{$issue->getAttribute("id")} + 1;
        }
        elsif ($issue->getAttribute("severity") eq "style"){
            push(@styleList, $issue);
            $styleID{$issue->getAttribute("id")} = $styleID{$issue->getAttribute("id")} + 1;
        }
        elsif ($issue->getAttribute("severity") eq "portability"){
            push(@portabilityList, $issue);
            $portabilityID{$issue->getAttribute("id")} = $portabilityID{$issue->getAttribute("id")} + 1;
        }
        elsif ($issue->getAttribute("severity") eq "information"){
            push(@informationList, $issue);
            $informationID{$issue->getAttribute("id")} = $informationID{$issue->getAttribute("id")} + 1;
        }
    }

    $anomalies{"error"} = \@errorList;
    $anomalies{"warning"} = \@warningList;
    $anomalies{"performance"} = \@performanceList;
    $anomalies{"style"} = \@styleList;
    $anomalies{"portability"} = \@portabilityList;
    $anomalies{"information"} = \@informationList;

    $idStruct{"error"} = \%errorID;
    $idStruct{"warning"} = \%warningID;
    $idStruct{"performance"} = \%performanceID;
    $idStruct{"style"} = \%styleID;
    $idStruct{"portability"} = \%portabilityID;
    $idStruct{"information"} = \%informationID;

    $returnValue{"anomalies"}=\%anomalies;
    $returnValue{"idStruct"}=\%idStruct;

    return %returnValue;
}




















sub drawPieChart{
    #Args: x, y, size, content, anomalyHandler
    my ($pieX, $pieY, $pieSize, $content, $totalAnomalies, %anomalies) = @_;

    if($totalAnomalies == 0){
        return;
    }

    my $errorPercent = scalar(@{$anomalies{'error'}})/$totalAnomalies;
    my $warningPercent = scalar(@{$anomalies{'warning'}})/$totalAnomalies;
    my $performancePercent = scalar(@{$anomalies{'performance'}})/$totalAnomalies;
    my $portabilityPercent = scalar(@{$anomalies{'portability'}})/$totalAnomalies;
    my $stylePercent = scalar(@{$anomalies{'style'}})/$totalAnomalies;
    my $informationPercent = scalar(@{$anomalies{'information'}})/$totalAnomalies;

    my $currentAngle = 90;

    if($errorPercent > 0){
        $content->fillcolor('red');
        $content->strokecolor('black');
        $content->pie($pieX, $pieY, $pieSize, $pieSize, $currentAngle, $currentAngle+$errorPercent*360);
        $content->fill();
        $content->pie($pieX, $pieY, $pieSize, $pieSize, $currentAngle, $currentAngle+$errorPercent*360);
        $content->stroke();
        $currentAngle += $errorPercent*360;
    }
    if($warningPercent > 0){
        $content->fillcolor('orange');
        $content->pie($pieX, $pieY, $pieSize, $pieSize, $currentAngle, $currentAngle+$warningPercent*360);
        $content->fill();
        $content->pie($pieX, $pieY, $pieSize, $pieSize, $currentAngle, $currentAngle+$warningPercent*360);
        $content->stroke();
        $currentAngle += $warningPercent*360;
    }
    if($performancePercent > 0){
        $content->fillcolor('yellow');
        $content->pie($pieX, $pieY, $pieSize, $pieSize, $currentAngle, $currentAngle+$performancePercent*360);
        $content->fill();
        $content->pie($pieX, $pieY, $pieSize, $pieSize, $currentAngle, $currentAngle+$performancePercent*360);
        $content->stroke();
        $currentAngle += $performancePercent*360;
    }
    if($portabilityPercent > 0){
        $content->fillcolor('green');
        $content->pie($pieX, $pieY, $pieSize, $pieSize, $currentAngle, $currentAngle+$portabilityPercent*360);
        $content->fill();
        $content->pie($pieX, $pieY, $pieSize, $pieSize, $currentAngle, $currentAngle+$portabilityPercent*360);
        $content->stroke();
        $currentAngle += $portabilityPercent*360;
    }
    if($stylePercent > 0){
        $content->fillcolor('blue');
        $content->pie($pieX, $pieY, $pieSize, $pieSize, $currentAngle, $currentAngle+$stylePercent*360);
        $content->fill();
        $content->pie($pieX, $pieY, $pieSize, $pieSize, $currentAngle, $currentAngle+$stylePercent*360);
        $content->stroke();
        $currentAngle += $stylePercent*360;
    }
    if($informationPercent > 0){
        $content->fillcolor('pink');
        $content->pie($pieX, $pieY, $pieSize, $pieSize, $currentAngle, $currentAngle+$informationPercent*360);
        $content->fill();
        $content->pie($pieX, $pieY, $pieSize, $pieSize, $currentAngle, $currentAngle+$informationPercent*360);
        $content->stroke();
        $currentAngle += $informationPercent*360;
    }
    $content->fillcolor('black');
}





sub processSettings{
    #ARG is DOM
    my $dom = @_[0];

    my @enableList = $dom->findnodes('/results/settings/enables');
    my @includeList = $dom->findnodes('/results/settings/includes');
    my @excludeList = $dom->findnodes('/results/settings/excludes');
    my @suppressionList = $dom->findnodes('/results/settings/suppressions');
    my @definesList = $dom->findnodes('/results/settings/defines');
    my @targetList = $dom->findnodes('/results/targets/target');

    $settingsContent = $settingsContent."Target(s):\n";
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

    return $settingsContent;
}


sub getNthMostOccurringID{
    my $n = shift(@_);
    my %hash = @_;
    my $list = "";
    foreach my $key (sort { $hash{$b} <=> $hash{$a}  or $b cmp $a } keys %hash){
        $n -= 1;
        $list = $list."\n".$key.": ".$hash{$key};
        if($n == 0){
            return $list;
        }
    }
    while($n != 0){
        $list = $list."\n ";
        $n--;
    }
    return $list;
}


sub drawStatisticsTables{
    #ARGS: pdf, page, anomaly handler, id handler, marginsize
    my ($pdf, $page, $anomalyHandle, $idHandle, $marginSize, $font) = @_;

    %anomalyHandler = %$anomalyHandle;
    %idHandler = %$idHandle;

    my @errorList = @{$anomalyHandler{'error'}};
    my @warningList = @{$anomalyHandler{'warning'}};
    my @performanceList = @{$anomalyHandler{'performance'}};
    my @portabilityList = @{$anomalyHandler{'portability'}};
    my @styleList = @{$anomalyHandler{'style'}};
    my @informationList = @{$anomalyHandler{'information'}};

    

    my $errorTable = [
        ["Errors: ".@errorList], [getNthMostOccurringID(5, %{$idHandler{"error"}})],
    ];

    my $warningTable = [
        ["Warnings: ".@warningList], [getNthMostOccurringID(5, %{$idHandler{"warning"}})],
    ];

    my $performanceTable = [
        ["Performance: ".@performanceList], [getNthMostOccurringID(5, %{$idHandler{"performance"}})],
    ];

    my $portabilityTable = [
        ["Portability: ".@portabilityList], [getNthMostOccurringID(5, %{$idHandler{"portability"}})],
    ];

    my $styleTable = [
        ["Style: ".@styleList], [getNthMostOccurringID(5, %{$idHandler{"style"}})],
    ];

    my $otherTable = [
        ["Other: ".@informationList], [getNthMostOccurringID(5, %{$idHandler{"information"}})],
    ];

    my $pdftable = new PDF::Table;
    $pdftable->table($pdf, $page, $errorTable, 'x' => $marginSize,'y' => 450, 'h' => 100, 'w' => '216', 'size' => '3in','font_size' => 10,'font' => $font,'justify' =>'center','max_word_length' => 70, 'header_props' => {'bg_color'=>'red', 'font_size' => 14});
    $pdftable->table($pdf, $page, $warningTable, 'x' => $marginSize+306,'y' => 450, 'h' => 100, 'w' => '216', 'size' => '3in','font_size' => 10,'font' => $font,'justify' =>'center','max_word_length' => 70, 'header_props' => {'bg_color'=>'orange', 'font_size' => 14});
    $pdftable->table($pdf, $page, $performanceTable, 'x' => $marginSize,'y' => 300, 'h' => 100, 'w' => '216', 'size' => '3in','font_size' => 10,'font' => $font,'justify' =>'center','max_word_length' => 70, 'header_props' => {'bg_color'=>'yellow', 'font_size' => 14});
    $pdftable->table($pdf, $page, $portabilityTable, 'x' => $marginSize+306,'y' => 300, 'h' => 100, 'w' => '216', 'size' => '3in','font_size' => 10,'font' => $font,'justify' =>'center','max_word_length' => 70, 'header_props' => {'bg_color'=>'green', 'font_size' => 14});
    $pdftable->table($pdf, $page, $styleTable, 'x' => $marginSize,'y' => 150, 'h' => 100, 'w' => '216', 'size' => '3in','font_size' => 10,'font' => $font,'justify' =>'center','max_word_length' => 70, 'header_props' => {'bg_color'=>'blue', 'font_size' => 14});
    $pdftable->table($pdf, $page, $otherTable, 'x' => $marginSize+306,'y' => 150, 'h' => 100, 'w' => '216', 'size' => '3in','font_size' => 10,'font' => $font,'justify' =>'center','max_word_length' => 70, 'header_props' => {'bg_color'=>'pink', 'font_size' => 14});
}



































1;