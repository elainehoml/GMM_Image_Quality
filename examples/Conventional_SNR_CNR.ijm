//-------------------------------------------//
// Script to select ROIs for conventional   //
// SNR and CNR calculation                  //
// Last edited: 11th Feb 2020               //
// eml.ho@soton.ac.uk                       //
//------------------------------------------//

function open_image() {
	// Open an image as a virtual stack
	// Closes other active images
	close("*");
	img_fname = File.openDialog("Select an image");
	open(img_fname, "virtual");
}

function random_slice() {
	// Display a randomly selected slice in the stack
	slice_no = round(random * nSlices);
	if (slice_no < 1 || slice_no > nSlices) {
		slice_no = round(random * nSlices);
	}
	else {
		setSlice(slice_no);
	}
}

function init_ROI() {
	// Draws an initial circular ROI to be
	// moved around by user
	makeOval(226, 185, 20, 20);
}

function select_ROI(material) {
	// Allow user to move ROI to specified material (str)
	// Measure mean and std dev, record ROI
	waitForUser("Please move ROI to " + material);
	roiManager("add");
}

function measure_material(material) {
	// Measures mean and std dev for ROIs (one row per ROI)
	run("Set Measurements...", "mean standard redirect=None decimal=3");
	roiManager("measure");
	IJ.renameResults(img_title + " " + material + " measurements");
	save_fname = img_dir + img_title + "_results/" + img_title + "_" + material;
	saveAs("Results", save_fname + "_mu_sigma.csv"); // save measurements
	print("Saving results as " + save_fname);
	roiManager("List");
	saveAs("Results", save_fname + "_ROI.csv"); // save ROIs
	close("*.csv");
	close("*measurements");
}

function select_measure_save_material(material) {
	roiManager("reset"); // Clear ROI manager
	for (i=0; i<5; i++) { //5 ROIs on random slices (1/slice)
		random_slice();
		init_ROI();
		select_ROI(material);
	}
	measure_material(material);
}

// MAIN ----------------------------------------
open_image();
img_dir = File.directory;
img_title = File.nameWithoutExtension;
select_measure_save_material("air");
select_measure_save_material("wax");
select_measure_save_material("tissue");