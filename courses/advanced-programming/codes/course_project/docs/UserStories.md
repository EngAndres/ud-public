# Course Project

This is a project to apply different concepts regarding _object-oriented design_, _RESTFul APIs_, and _Model-Template-Controller_.

## Business Model

This is an application to emulate an online video game services platform. It means, buy/exchange video games, buy tockens, new launches, among others.


## User Stories

- As manager, I want to see who are the current online players, so what we can notify news.
- As player, I want to see the videogames catalog, so what I can make a buy decision.
- As player, I want to see videogames categories, so what videogames searches could be more specific.
- As player, I want to chat with other players, so what I could create player/community groups.
- As player, I want to create an account, so what I can save preferences and videogames progress.
- As seller, I want to create an account, so what I can publish videogames to sell.
- As seller, I want to have a registered bank account, so what I can receive payments for videogames selling.
- As manager, I want to add a mark to new video games, so what I can define the list of new launches.
- As seller, I want modify the information related with a videogame, so what I can provide updates to increase sells.

## Entities

- Manager: name
- Players: name, alias, age, online/offline, make search, write chat, preferences, progress, [banck account]
- News
- VideoGames: category, new_launch
- Catalog
- Category
- Group (community)
- Seller: list to sell, banck account 
- BankAccount

## Process


## Web Services

- login -> User.login   POST  {username, password}
- createPlayer -> Player   POST  {age, name, alias, bank_account{name, number}}
- createSeller -> Seller   POST {}
- createManager -> Manager   POST {}
- markVideoGame -> Manager.mark_videogame    PUT {code}
- registerPlatformNews -> Manager.register_news   POST  {title, publish_date, description, deadline}
- deactivatePlatformNews -> Manager.deactive_news    PUT {title}
- buyVideoGame -> Player.buy_videogame   POST    {code}
- publishVideoGame -> Seller.publish_videogame  POST {code, name, description, price}
- updateVideoGame -> Seller.update_videogame   PUT {}
- createCommunity -> Community  POST {name}
- showCategories -> Catalog.show_categories   GET
- showByCategory -> Catalog.show_by_category    GET {?category=...}
- showNewLaunches -> Catalog.show_new_launches GET