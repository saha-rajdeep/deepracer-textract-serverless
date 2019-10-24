# deepracer-textract-serverless
Analyses deepracer race result image, extracts the team name, laptime and circuit name and dumps into s3 in csv format. Quicksight leaderboard is created from the S3

Full AWS Native Serverless solution, no front end UI experience required!
Steps:
1. Run the SAM_template in cloudformation (No need to clone repo)
2. This will spin up lambda, SNS, two S3 buckets - one to put image in, another to save the results
3. Lambda code is given in repo for reference, cloudformation picks up from s3 buckets
4. Cloudformation output shows S3BucketForImage and S3BucketForResult
5. Event Trigger is also set for the lambda to get triggered anytime an image is placed in S3BucketForImage
6. Sample, expected screenshot also included for reference(good_deepracer_image.png)
7. Take screenshot of the time of your public race and upload to S3BucketForImage
8. resulting CSV will be put in S3 S3BucketForResult. Sample CSV shown - SimonR-NYC_2019-10-23T04-38-24-355905.csv
9. Create quicksight leaderboard pointting to S3BucketForResult
10. PROFIT!
 