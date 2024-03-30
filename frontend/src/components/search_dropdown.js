import React, { useState } from 'react';
import style from './style.module.css';

const SearchableDropdown = ({items, selectedItem, setSelectedItem, custom_prompt}) => {
  const [filteredItems, setFilteredItems] = useState(items);
  const [showDropdown, setShowDropdown] = useState(false);

  const handleInputChange = (e) => {
    setSelectedItem(e.target.value)
    const inputVal = e.target.value.toLowerCase();
    const filtered = items.filter(item => item.toLowerCase().includes(inputVal));
    setFilteredItems(filtered);
  };

  const handleSelectItem = (selectedItem) => {
    setSelectedItem(selectedItem);
    setShowDropdown(false);
  };

  return (
    <div className={style.searchable_dropdown}>
        <input className={style.input} type="text" placeholder={custom_prompt} value={selectedItem} onChange={handleInputChange}
            onFocus={() => setShowDropdown(true)} 
            onBlur={() => setTimeout(() => setShowDropdown(false), 150)}
        />
    {showDropdown && (
        <div className={style.dropdown_menu}>
        {filteredItems.slice(0, 7).map((item, index) => (
            <div key={index} className={style.dropdown_item} onClick={() => {handleSelectItem(item);}}> 
                {item}
            </div>
        ))}
    </div>
      )}
    </div>
  );
};

export default SearchableDropdown;
