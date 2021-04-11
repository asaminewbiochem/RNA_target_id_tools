#!/usr/bin/env nextflow
//echo false

//parameters

//gapdh plus strand
params.GENOME="/home/ahaile/RNA-J/data/GRCh38.primary_assembly.genome.fa"
params.GFF3="/home/ahaile/RNA-J/data/hg38.gff3.gz"
params.CODEPATH="/home/ahaile/RNA-J/revirtx"

params.OUT="rna"


probingFlag=params.probe.split("\s+|,")

println probingFlag
if ("probewdms" in probingFlag){
        params.OUTDIR="RNA_results-dms"
}else if("probewshape" in probingFlag){
        params.OUTDIR="RNA_results-shape"
}else if("noprobe" in probingFlag){
        params.OUTDIR="RNA_results-none"
}



params.process="Fold"

TR = Channel.from(file(params.TR).text.split())
SHAPEBW = Channel.from(file(params.SHAPEBW).text.split())
REGION = Channel.from("five_prime_UTR","three_prime_UTR","CDS")

processFlag=params.process.split("\s+|,")

println processFlag
if ("Fold" in processFlag){
	println "Fold flag on"
}else if("ShapeKnots" in processFlag){
	println "ShapeKnots flag on"
}

subTR = { it.split("---")[0] }
subRegion = { it.split("---")[1] }
subShape = { it.split("---")[2] }

getname = {it.replaceAll(".bw","").replaceAll(".*\\/","")}

log.info """\
 RNA Structure Prediction
 ===================================
 Genome: ${params.GENOME}
 GFF3: ${params.GFF3}
 SHAPEBW = ${params.SHAPEBW}
 """
 .stripIndent()


//get rna fasta in gff format
process getfata {
	tag "${tr} ${rg}"
	publishDir "$params.OUTDIR/${tr}"

	input:
	val tr from TR
	each rg from REGION

	output:
	file("${tr}---${rg}.bed") into BED

	shell:
	'''
	python !{params.CODEPATH}/getrna.py -t !{rg} !{tr} !{params.GFF3} !{params.GENOME} -b bedOut -o rna.gff
	python !{params.CODEPATH}/bedperbase.py rna.gff > !{tr}---!{rg}.bed
	'''
}

//shape bigwig to bedgraph
process getshape {
	tag "${getname(bw)}"
	input:
	val bw from SHAPEBW
	output:
	file "${getname(bw)}.bedgraph" into SHAPESCORE	

	shell:
	'''	
	bigWigToBedGraph !{bw} !{getname(bw)}.bedgraph
	'''
}

//merge with shape data
//prep for rnastructure
process mergeFastaShape {
	publishDir "$params.OUTDIR/${subTR(bed.baseName)}/${subRegion(bed.baseName)}/${shape.baseName}"

	input:
	each file(bed) from BED
	each file(shape) from SHAPESCORE
	output:
	file("${bed.baseName}---${shape.baseName}.fa") into PREDFA_Fold, PREDFA_ShapeKnots
	file("${bed.baseName}---${shape.baseName}.shape") into PREDSHAPE_Fold, PREDSHAPE_ShapeKnots

	shell:	
	'''
	bedtools intersect -a !{bed} -b !{shape} -loj > rna_joined.bed
	python !{params.CODEPATH}/formatFaShape.py rna_joined.bed -f !{bed.baseName}---!{shape.baseName}.fa -s !{bed.baseName}---!{shape.baseName}.shape
	'''
}

//predict RNA struture
process Fold{
	label "heavy"
	publishDir "$params.OUTDIR/${subTR(fa.baseName)}/${subRegion(fa.baseName)}/${subShape(fa.baseName)}/Fold"
	maxForks = 1
	time '4h'
	errorStrategy 'ignore'
	input:
	file(fa) from PREDFA_Fold
	file(shape) from PREDSHAPE_Fold

	output:
	file "${fa.baseName}.ct" into CT_Fold
	file "${shape.baseName}.ps" into PS_Fold
        file "${shape.baseName}.1.dot" into DOT1_Fold
        file "${shape.baseName}.2.dot" into DOT2_Fold
        file "${shape.baseName}.3.dot" into DOT3_Fold
        file "${shape.baseName}.1.png" into PNG1_Fold
        file "${shape.baseName}.2.png" into PNG2_Fold
        file "${shape.baseName}.3.png" into PNG3_Fold

	when:
	"Fold" in processFlag 

	shell:
        '''
        
        if [ !{params.probe} == "noprobe" ];then 
        Fold-smp !{fa} !{fa.baseName}.ct -m 3
        elif [ !{params.probe} == "probewdms" ];then
        Fold-smp !{fa} !{fa.baseName}.ct -m 3 -dms !{shape}
        elif [ !{params.probe} == "probewshape" ];then
        Fold-smp !{fa} !{fa.baseName}.ct -m 3 -sh !{shape}
        fi
        draw !{fa.baseName}.ct !{shape.baseName}.ps -s !{shape}
        ct2dot !{fa.baseName}.ct 1 !{fa.baseName}.1.dot
        ct2dot !{fa.baseName}.ct 2 !{fa.baseName}.2.dot
        ct2dot !{fa.baseName}.ct 3 !{fa.baseName}.3.dot
        python /home/ahaile/RNA-J/forgi/examples/rnaConvert.py !{fa.baseName}.1.dot -T neato | neato -Tpng -o !{fa.baseName}.1.png
        python /home/ahaile/RNA-J/forgi/examples/rnaConvert.py !{fa.baseName}.2.dot -T neato | neato -Tpng -o !{fa.baseName}.2.png
        python /home/ahaile/RNA-J/forgi/examples/rnaConvert.py !{fa.baseName}.3.dot -T neato | neato -Tpng -o !{fa.baseName}.3.png
        '''


}


process ShapeKnots{
        label "heavy"
        publishDir "$params.OUTDIR/${subTR(fa.baseName)}/${subRegion(fa.baseName)}/${subShape(fa.baseName)}/ShapeKnots"
        maxForks = 1
        time '4h'
        errorStrategy 'ignore'

        input:
        file(fa) from PREDFA_ShapeKnots
        file(shape) from PREDSHAPE_ShapeKnots

        output:
        file "${fa.baseName}.ct" into CT_ShapeKnots
        file "${shape.baseName}.ps" into PS_ShapeKnots
        file "${shape.baseName}.1.dot" into DOT1_ShapeKnots
        file "${shape.baseName}.2.dot" into DOT2_ShapeKnots
        file "${shape.baseName}.3.dot" into DOT3_ShapeKnots
        file "${shape.baseName}.1.png" into PNG1_ShapeKnots
        file "${shape.baseName}.2.png" into PNG2_ShapeKnots
        file "${shape.baseName}.3.png" into PNG3_ShapeKnots
        when:
        "ShapeKnots" in processFlag 

        shell:
        '''
        if [ !{params.probe} == "noprobe" ];then
        ShapeKnots-smp !{fa} !{fa.baseName}.ct -m 3
        elif [ !{params.probe} == "probewdms" ];then
        ShapeKnots-smp !{fa} !{fa.baseName}.ct -m 3 -dms !{shape}
        elif [ !{params.probe} == "probewshape" ];then
        ShapeKnots-smp !{fa} !{fa.baseName}.ct -m 3 -sh !{shape}
        fi

        draw !{fa.baseName}.ct !{shape.baseName}.ps -s !{shape}
        ct2dot !{fa.baseName}.ct 1 !{fa.baseName}.1.dot
        ct2dot !{fa.baseName}.ct 2 !{fa.baseName}.2.dot
        ct2dot !{fa.baseName}.ct 3 !{fa.baseName}.3.dot
        python /home/ahaile/RNA-J/forgi/examples/rnaConvert.py !{fa.baseName}.1.dot -T neato | neato -Tpng -o !{fa.baseName}.1.png
        python /home/ahaile/RNA-J/forgi/examples/rnaConvert.py !{fa.baseName}.2.dot -T neato | neato -Tpng -o !{fa.baseName}.2.png
        python /home/ahaile/RNA-J/forgi/examples/rnaConvert.py !{fa.baseName}.3.dot -T neato | neato -Tpng -o !{fa.baseName}.3.png
        '''
}
