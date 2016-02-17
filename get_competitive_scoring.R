library(ggplot2)

files <- list.files(path="~/Analytics/nd_basketball/competitive_lineup_plays", pattern="*.csv", full.names=T, recursive=FALSE)
all_plays <- NULL
nd_score_dif <- 0

players <- c("auguste","beachem","burgett","burns","colson","farrell","geben","gregory","holtz","jackson","pflueger","ryan","torres","vasturia")
player_seconds <- vector(mode = "integer", length = length(players))
player_margins <- vector(mode = "integer", length = length(players))
names(player_seconds) <- players
names(player_margins) <- players

for (file in files) {
  #Get the name of the particular file
  file_split <- strsplit(file, "/")
  filename <- tail(file_split[[1]], n=1)
  file_split <- strsplit(filename,".",fixed=TRUE)
  filename <- file_split[[1]][1]
  
  plays <- read.csv(file)
  plays$margin_change_for_nd <- 0
  
  nd_is_home <- FALSE
  if(plays$home_team[1] == "NOTRE DAME")
    nd_is_home <- TRUE
  
  
  #Find each player's minutes
  for (player in players) {
    player_sec_this_game <- 0
    player_entered_min <- 20
    player_entered_sec <- 0
    i <- 2
    while (i <= nrow(plays)) {
      #At the beginning of the second half, credit players who were still in at the end
      #of the first half and reset the starting times of players
      if (plays$half[i-1] == 1 & plays$half[i] == 2) {
        if (plays[i-1,player] == 1) {
          minutes_in <- player_entered_min - 0
          seconds_in <- player_entered_sec - 0
          player_sec_this_game <- player_sec_this_game + 60 * minutes_in + seconds_in
        }
        player_entered_min <- 20
        player_entered_sec <- 0
      }
      
      #If the player comes into the game
      if (plays[i-1,player] == 0 & plays[i,player] == 1) {
        player_entered_min <- plays$minute[i]
        player_entered_sec <- plays$second[i]
      } else if (plays[i-1,player] == 1 & plays[i,player] == 0) {
        #If the player comes out of the game
        minutes_in <- player_entered_min - plays$minute[i]
        seconds_in <- player_entered_sec - plays$second[i]
        player_sec_this_game <- player_sec_this_game + 60 * minutes_in + seconds_in
      }
      
      i <- i + 1
    }
    
    #When the game ends, credit whoever is still in with minutes
    if (plays[i-1,player] == 1) {
      minutes_in <- player_entered_min - 0
      seconds_in <- player_entered_sec - 0
      player_sec_this_game <- player_sec_this_game + 60 * minutes_in + seconds_in
    }
    
    if(player_sec_this_game > 60 * 40) {
      print("\nToo many minutes")
      print(player)
      print(filename)
    }
    
    #add the new player seconds to the running total
    player_seconds[player] <- player_seconds[player] + player_sec_this_game
  }
  
  #Calculate net plus/minus
  i <- 2
  while (i <= nrow(plays)) {
    #Calculate the change in score from ND's perspective
    margin_change_for_home <- plays$home_score[i] - plays$home_score[i-1]
    margin_change_for_away <- plays$away_score[i] - plays$away_score[i-1]
    if (nd_is_home)
      plays$margin_change_for_nd[i] <- margin_change_for_home - margin_change_for_away
    else
      plays$margin_change_for_nd[i] <- margin_change_for_away - margin_change_for_home
    
    #Be sure the change in score makes sense
    if(plays$margin_change_for_nd[i] > 3 | plays$margin_change_for_nd[i] < -3) {
      print("Error: Scoring Margin should not be so large")
    }
    
    #For each player who was in on the play, increment his plus/minus
    if (plays$margin_change_for_nd[i] != 0)
      for (player in players)
        if (plays[i, player])
          player_margins[player] <- player_margins[player] + plays$margin_change_for_nd[i]
    
    i <- i + 1
  }
  
  #increment Notre Dame's total scoring differential
  if(nd_is_home)
    nd_score_dif <- nd_score_dif + plays$home_score[i-1] - plays$away_score[i-1]
  else
    nd_score_dif <- nd_score_dif - plays$home_score[i-1] + plays$away_score[i-1]
  
  if (exists("all_plays"))
    all_plays <- rbind(all_plays,plays)
  else
    all_plays <- plays
}


par(mar=c(4,7,2,1))
#Capitalize the names for the plots
names(player_seconds) <- c("Auguste","Beachem","Burgett","Burns","Colson","Farrell","Geben","Gregory","Holtz","Jackson","Pflueger","Ryan","Torres","Vasturia")
names(player_margins) <- c("Auguste","Beachem","Burgett","Burns","Colson","Farrell","Geben","Gregory","Holtz","Jackson","Pflueger","Ryan","Torres","Vasturia")
#Plot
min_and_margin <- data.frame(player_seconds/60,player_margins)
min_and_margin$player_minutes <- min_and_margin$player_seconds.60
min_and_margin$player_seconds.60 <- NULL
min_and_margin <- min_and_margin[order(min_and_margin$player_minutes),]
barplot(min_and_margin$player_minutes, col = c(1,1,1,1,1,1,1,1,1,3,3,3,3,3), horiz = TRUE, main = "Minutes by Player", las = 1, names.arg= rownames(min_and_margin))
barplot(min_and_margin$player_margins, col = c(1,1,1,1,1,1,1,1,1,3,3,3,3,3), horiz = TRUE, main = "Net Margin by Player", las = 1, names.arg=rownames(min_and_margin))
min_and_margin$margin_per_40 <- min_and_margin$player_margins / min_and_margin$player_minutes * 40
min_and_margin <- min_and_margin[which(min_and_margin$player_minutes > 0),]
min_and_margin <- min_and_margin[order(min_and_margin$margin_per_40),]
barplot(min_and_margin$margin_per_40, col = c(1,1,3,3,3,3,3,1,1,1,1), horiz = TRUE, main = "Margin per 40 Minutes", las = 1, names.arg=rownames(min_and_margin))
min_and_margin$off_court_margin <- nd_score_dif - min_and_margin$player_margins
nd_total_minutes <- 40 * length(files)
min_and_margin$off_court_margin_per_40 <- min_and_margin$off_court_margin / (nd_total_minutes - min_and_margin$player_minutes) * 40
min_and_margin$plusminus_per_40 <- min_and_margin$margin_per_40 - min_and_margin$off_court_margin_per_40
min_and_margin <- min_and_margin[order(min_and_margin$plusminus_per_40),]
barplot(min_and_margin$plusminus_per_40, col = c(1,1,3,1,3,3,1,3,3,1,1), horiz = TRUE, main = "Plus/Minus per 40 Minutes (Competitive Games)", las = 1, names.arg=rownames(min_and_margin))
barplot(min_and_margin$plusminus_per_40[-1][-1], col = c(3,1,3,3,1,3,3,1,1), horiz = TRUE, main = "Plus/Minus per 40 Minutes (Competitive Games)", las = 1, names.arg=rownames(min_and_margin)[-1][-1])
