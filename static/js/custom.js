document.addEventListener("DOMContentLoaded", function() {
    var categorySelect = document.querySelector('select[name="category"]');  // Dropdown for existing categories
    var newCategoryInput = document.getElementById('newCategoryInput');      // Input for new category

    // Disable dropdown if the input has value, and vice versa
    newCategoryInput.addEventListener('input', function() {
        if (newCategoryInput.value.trim() !== '') {
            categorySelect.disabled = true;  // Disable dropdown when input is filled
        } else {
            categorySelect.disabled = false;  // Enable dropdown when input is empty
        }
    });

    // Disable input if the dropdown is selected
    categorySelect.addEventListener('change', function() {
        if (categorySelect.value !== '') {
            newCategoryInput.disabled = true;  // Disable input when dropdown is selected
        } else {
            newCategoryInput.disabled = false;  // Enable input when no category is selected
        }
    });
});