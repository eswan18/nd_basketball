library(stringr)

#Open each raw plays file
files <- list.files(path="~/Analytics/nd_basketball/fixed_plays", pattern="*.csv", full.names=T, recursive=FALSE)
for (file in files) {
  #Get the name of the particular file
  file_split <- strsplit(file, "/")
  filename <- tail(file_split[[1]], n=1)
  file_split <- strsplit(filename,".",fixed=TRUE)
  filename <- file_split[[1]][1]

  plays <- read.csv(file)
  
  #Set up dummy variables for later
  plays$auguste <- 0
  plays$beachem <- 0
  plays$burgett <- 0
  plays$burns <- 0
  plays$colson <- 0
  plays$farrell <- 0
  plays$geben <- 0
  plays$gregory <- 0
  plays$holtz <- 0
  plays$jackson <- 0
  plays$pflueger <- 0
  plays$ryan <- 0
  plays$torres <- 0
  plays$vasturia <- 0
  
  #Check if ND is home or away (so we know which play column to read)
  home_team <- as.character(plays$home_team[[1]])
  nd_is_home <- FALSE
  if(home_team == "NOTRE DAME") {
    nd_is_home <- TRUE
  }
  
  #Order the data frame by half asc, minute desc, second desc, home score asc, away score asc
  plays <- plays[order(plays$half,-plays$minute,-plays$second,plays$home_score,plays$away_score),]
  
  #Add in the starters
  starter_list <- list("Bonzie Colson", "Steve Vasturia", "Demetrius Jackson", "V.J. Beachem", "Zach Auguste")
  starter_list_2 <- list("Matt Ryan", "Steve Vasturia", "Demetrius Jackson", "V.J. Beachem", "Zach Auguste")
  starter_list_3 <- list("Bonzie Colson", "Steve Vasturia", "Rex Pflueger", "V.J. Beachem", "Zach Auguste")
  starter_list_4 <- list("A.J. Burgett", "Steve Vasturia", "Demetrius Jackson", "V.J. Beachem", "Zach Auguste")
  
  if(filename %in% list("game-16","du0116","game-18","game-19")) {
    starter_list <- starter_list_2
  } else if (filename %in% list("game-20")) {
    starter_list <- starter_list_3
  } else if (filename %in% list("game-21","game-22")) {
    starter_list <- starter_list_4
  }
  
  #Find who is on the floor for each play
  current_lineup <- starter_list
  lineups <- vector(mode="list", length=nrow(plays))
  
  #Parse plays that are substitutions
  i = 1
  first_play_of_second_half <- TRUE
  while (i <= nrow(plays)) {
    #Reset to starters at the beginning of the second half - a bit hacky
    if (plays[i,]$half == 2 & first_play_of_second_half) {
      current_lineup <- starter_list
      first_play_of_second_half <- FALSE
    }
    #Get the right play column for ND
    if(nd_is_home)
      current_play <- as.character(plays[i,]$home_play)
    else
      current_play <- as.character(plays[i,]$away_play)
    
    #Check if it is a substitution and adjust current_lineup if so
    if(!is.null(current_play) & length(current_play) > 0)
       if(grepl("SUB IN", current_play)) {
         player_split <- strsplit(current_play, " : ", fixed = TRUE)
         player_in <- player_split[[length(player_split)]][2]
         
         #If the player isn't currently on the floor, add him to the lineup
         if (!(player_in %in% current_lineup)) {
           current_lineup <- append(current_lineup,player_in)
         }
         
       } else if(grepl("SUB OUT", current_play)) {
         player_split <- strsplit(current_play, ": ", fixed = TRUE)
         player_out <- player_split[[length(player_split)]][2]
         
         #If the player is currently on the floor, remove him from the lineup
         if (player_out %in% current_lineup) {
           current_lineup <- current_lineup[-which(current_lineup == player_out)]
         }
       }
    
    #Fun part: convert the current lineup to dummy variables
    if("Zach Auguste" %in% current_lineup) {
      plays$auguste[i] <- 1
    } else {
      plays$auguste[i] <- 0
    }
    if("V.J. Beachem" %in% current_lineup) {
      plays$beachem[i] <- 1
    } else {
      plays$beachem[i] <- 0
    }
    #Burgett is listed as either A.J. or Austin depending on the game
    if("A.J. Burgett" %in% current_lineup | "Austin Burgett" %in% current_lineup) {
      plays$burgett[i] <- 1
    } else {
      plays$burgett[i] <- 0
    }
    if("Elijah Burns" %in% current_lineup) {
      plays$burns[i] <- 1
    } else {
      plays$burns[i] <- 0
    }
    if("Bonzie Colson" %in% current_lineup) {
      plays$colson[i] <- 1
    } else {
      plays$colson[i] <- 0
    }
    if("Matt Farrell" %in% current_lineup) {
      plays$farrell[i] <- 1
    } else {
      plays$farrell[i] <- 0
    }
    if("Martinas Geben" %in% current_lineup) {
      plays$geben[i] <- 1
    } else {
      plays$geben[i] <- 0
    }
    if("Matt Gregory" %in% current_lineup) {
      plays$gregory[i] <- 1
    } else {
      plays$gregory[i] <- 0
    }
    if("Chad Holtz" %in% current_lineup) {
      plays$holtz[i] <- 1
    } else {
      plays$holtz[i] <- 0
    }
    if("Demetrius Jackson" %in% current_lineup) {
      plays$jackson[i] <- 1
    } else {
      plays$jackson[i] <- 0
    }
    if("Rex Pflueger" %in% current_lineup) {
      plays$pflueger[i] <- 1
    } else {
      plays$pflueger[i] <- 0
    }
    if("Matt Ryan" %in% current_lineup) {
      plays$ryan[i] <- 1
    } else {
      plays$ryan[i] <- 0
    }
    if("Austin Torres" %in% current_lineup) {
      plays$torres[i] <- 1
    } else {
      plays$torres[i] <- 0
    }
    if("Steve Vasturia" %in% current_lineup) {
      plays$vasturia[i] <- 1
    } else {
      plays$vasturia[i] <- 0
    }
    
    lineups[i] <- list(current_lineup)
    i = i + 1
  }
  #print(length(current_lineup))
  write.csv(plays, paste("~/Desktop/lineup_plays/", filename, ".csv", sep = ""))
}