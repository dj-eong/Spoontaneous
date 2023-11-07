
const BASE_URL = 'https://www.themealdb.com/api/json/v1/1/';

document.addEventListener('DOMContentLoaded', async function () {
    const list = await getIngredientsList();

    const input = document.querySelector('#search');
    const searchForm = document.querySelector('#searchform');

    searchForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        document.querySelector('main').innerText = '';
        //fuzzy search
        const results = fuzzysort.go(input.value, list, {
            threshold: -1000,
            limit: 1,
            all: false,
            key: null,
            keys: null,
            scoreFn: null
        });
        if (results[0]?.target) {
            const inp = document.createElement('p');
            console.log('The ingredient you searched for is ' + results[0].target);
            document.querySelector('main').append(inp);
            const recipe = await getMealRecipe(formatIngredient(results[0].target));
            if (recipe) displayRecipe(recipe);
        } else {
            const p = document.createElement('p');
            p.innerText = 'No recipe found with this ingredient';
            p.setAttribute('class', 'text-center');
            document.querySelector('main').append(p);
        }
        input.value = '';
    });
});

// get api list of ingredients
async function getIngredientsList() {
    const res = await axios.get(BASE_URL + 'list.php?i=list');
    // const list = [];
    // for (let meal of res.data.meals) {
    //     list.push(meal.strIngredient);
    // }
    // return list;
    return res.data.meals.map(function (meal) {
        return meal.strIngredient;
    });
}

// replace any spaces with underscores
function formatIngredient(ingredient) {
    const str = ingredient.replace(' ', '_');
    return str;
}

// get meals that include ingredient, pick random meal, get recipe
async function getMealRecipe(ingredient) {
    const res = await axios.get(BASE_URL + 'filter.php?i=' + ingredient);
    if (!res.data.meals) {
        return false;
    }
    const mealId = res.data.meals[Math.floor(Math.random() * res.data.meals.length)].idMeal;
    const rec = await axios.get(BASE_URL + 'lookup.php?i=' + mealId);
    return rec.data.meals[0];
}

// display meal and recipe on DOM
async function displayRecipe(recipe) {
    const main = document.querySelector('main');
    main.setAttribute('class', 'container my-5');

    const div = document.createElement('div');
    div.setAttribute('class', 'card custom-color recipe-container');
    main.append(div);
    const heading = document.createElement('h2');
    heading.innerText = recipe.strMeal;
    heading.setAttribute('class', 'card-header text-color text-center d-flex justify-content-between');
    div.append(heading);
    const img = document.createElement('img');
    img.setAttribute('src', recipe.strMealThumb);
    img.setAttribute('class', 'recipe-image');
    div.append(img);
    const heading2 = document.createElement('h3');
    heading2.innerText = 'Ingredients';
    heading2.setAttribute('class', 'text-color mt-1 mb-0');
    div.append(heading2);

    const ul = document.createElement('ul');
    ul.setAttribute('class', 'ingredients-list');
    div.append(ul);
    for (let i = 1; i <= 20; i++) {
        if (recipe[`strIngredient${i}`]) {
            const li = document.createElement('li');
            li.innerText = recipe[`strMeasure${i}`] + ' ' + recipe[`strIngredient${i}`];
            li.setAttribute('class', 'ingr-item');
            ul.append(li);
        }
    }
    const heading3 = document.createElement('h3');
    heading3.innerText = 'Instructions';
    heading3.setAttribute('class', 'text-color mt-0 mb-0');
    div.append(heading3);
    const instructions = document.createElement('p');
    instructions.innerHTML = recipe.strInstructions;
    instructions.setAttribute('class', 'instructions text-color');
    div.append(instructions);

    if (main.getAttribute('data')) {
        const res = await axios.get('/api/saved-recipes');
        if (res.data.includes(parseInt(recipe.idMeal))) {
            displayUnsaveButton(recipe.idMeal);
        } else {
            displaySaveButton(recipe.idMeal);
        }
    }
}

function displaySaveButton(recipeId) {
    const saveForm = document.createElement('form');

    const saveButton = document.createElement('button');
    saveButton.innerText = 'Save Recipe';
    saveButton.setAttribute('class', "btn btn-rounded color");
    saveForm.append(saveButton);
    document.querySelector('h2').append(saveForm);

    saveForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        displayUnsaveButton(recipeId);
        saveButton.remove();

        try {
            await axios.post(`/saved-recipes/${recipeId}`);
        } catch (error) {
            saveForm.append('Already saved!');
        }
    });
}

function displayUnsaveButton(recipeId) {
    const unsaveForm = document.createElement('form');

    const unsaveButton = document.createElement('button');
    unsaveButton.innerText = 'Unsave Recipe';
    unsaveButton.setAttribute('class', "btn btn-rounded color");
    unsaveForm.append(unsaveButton);
    document.querySelector('h2').append(unsaveForm);

    unsaveForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        displaySaveButton(recipeId);
        unsaveButton.remove();

        try {
            await axios.delete(`/saved-recipes/${recipeId}`);
        } catch (error) {
            unsaveForm.append('It was never saved!');
        }
    });
}