import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

import weka.core.Instances;
import weka.classifiers.evaluation.Evaluation;
import weka.classifiers.functions.SMOreg;

public class SMOregressor1 {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception{
		FileReader freader = new FileReader("/home/yongfeng/ML/Project/train.arff");
		BufferedReader breader = new BufferedReader(freader);
		Instances train = new Instances(breader);
		train.setClassIndex(0);
		breader.close();
		freader=null;
		breader=null;
		freader = new FileReader("/home/yongfeng/ML/Project/test.arff");
		breader = new BufferedReader(freader);
		Instances test = new Instances(breader);
		test.setClassIndex(0);
		breader.close();
		
		//final int CVfold = 3;
		final int sizeOfSearch1 = 60;
		final int sizeOfSearch2 = 8;
		double[][] resultsArray = new double[sizeOfSearch1][sizeOfSearch2];
		//BufferedWriter writer = new BufferedWriter(new FileWriter("SMOResults"));
		for (int i=0;i < sizeOfSearch1;i++){
			for(int j=0;j < sizeOfSearch2;j++){
				float c = i + 1;
				int gval = j-5;
				double gamma = Math.pow(10, gval);
				SMOreg smo = new SMOreg();
				String options = String.format("-C %f -N 0 -I \"weka.classifiers.functions.supportVector.RegSMOImproved -L 0.001 -W 1 -P 1.0E-12 -T 0.001 -V\" -K \"weka.classifiers.functions.supportVector.RBFKernel -C 250007 -G %f\"", c, gamma);
				smo.setOptions(weka.core.Utils.splitOptions(options));
				smo.buildClassifier(train);
				Evaluation eval = new Evaluation(train);
				eval.evaluateModel(smo, test);
				//eval.crossValidateModel(smo, train, CVfold, new Random(1));
				double error = eval.errorRate();
				System.out.println("Comlexity: " + c + "\tgamma: " + gamma + "\tError: " + error);
				//printOptions(smo.getOptions());
				resultsArray[i][j] = error;
				smo = null;
				eval = null;
			}
	}
		System.out.println();
		print(resultsArray);
		writeToFile("SMOResults",resultsArray);
		//findOptimal(resultsArray, "SMOResults");
	  
	}
	public static void findOptimal(double array[][], String filename) throws IOException{
		double mini = array[0][0];
		int x = 0;int y = 0;
		for(int i=0;i < array.length;i++){
			for(int j=0;j < array[0].length;j++){
				if(array[i][j] < mini){
					mini = array[i][j];
					x = i;
					y = j;
				}
			}
		}
		System.out.println("minimum error rate: " + mini);
		System.out.println("location: " + "(" + x + "," + y + ")");
		BufferedWriter writer = null;
		try {
			writer = new BufferedWriter(new FileWriter(filename, true));
			writer.append("minimum error rate: " + mini + "  at location" + "(" + x + "," + y + ")");
			writer.flush();
		} catch (IOException ex) {
			ex.printStackTrace();
		}finally{
			if(writer != null){
				writer.close();
			}
		}
		
	}
	public static void print(double[][] array){
		for(int i=0;i < array.length;i++){
			for(int j=0;j < array[0].length;j++){
				System.out.print(array[i][j] + "\t");
			}
			System.out.println();
		}	
	  }
	public static void printOptions(String[] options){
		for(int i=0;i < options.length;i++){
			System.out.print(options[i] + "\t");
		}
		System.out.println();
	  }
	public static void writeToFile(String filename, double[][] array) throws IOException{
		BufferedWriter writer = null;
		try{
			writer = new BufferedWriter(new FileWriter(filename));
			for(int i = 0;i < array.length;i++){
				for(int j = 0;j < array[0].length;j++){
					writer.write(Double.toString(array[i][j]) + "   ");
				}
				writer.newLine();
			}
			writer.flush();

		}catch(IOException ex){
			ex.printStackTrace();
		}finally{
			if(writer!=null){
				writer.close();
			}
		}
	  }
}
